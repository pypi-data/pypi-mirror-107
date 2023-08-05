from coopui.cli.CliAtomicUserInteraction import CliAtomicUserInteraction
from coopgantt.build_and_schedule_gantt import build_and_schedule
from coopgantt import build_html, build_svgs, Resource
import logging
from configparser import ConfigParser

class UserOperations:
    def __init__(self,
                 user_interaction: CliAtomicUserInteraction,
                 config_file_path: str = None):
        self.ui = user_interaction
        self.gantt = None
        self.gantt_name = ""
        self.task_filepath = None
        self.resources_filepath = None
        self.html_output_path = None
        self.svg_renderings_dir = None
        self.out_file = None
        self.project_priorities_filepath = None
        self.config_filepath = config_file_path

        if self.config_filepath is not None:
            self._load_from_config()

    def _get_task_data(self, task_filepath: str = None):
        task_columns = {
            'id': int,
            'project': str,
            'activity_type': str,
            'activity': str,
            'actual_start_date': str,
            'duration_days': int,
            'resources': str,
            'perc_done': int,
            'dependencies': str,
            'priority': int,
            'state': str,
            'sub_activities': str,
            'target_completion_date': str,
            'closed_date': str,
            'scheduled_start_date': str,
            'dont_start_before_date': str
        }

        task_data = self.ui.request_data_from_csv_with_specified_columns(task_columns, title="Gantt Activities",
                                                                         filepath=task_filepath)

        if task_data is None: return None

        task_data = task_data.fillna('')
        task_data = task_data.replace('nan', '')

        return task_data

    def _get_resource_data(self, resources_filepath: str = None):
        resources_columns = {
            'resource': str,
            'capacity': int,
            'max_by_project': str
        }
        resources_df = self.ui.request_data_from_csv_with_specified_columns(resources_columns, title="Resources", filepath=resources_filepath)
        if resources_df is None: return
        resources_df = resources_df.fillna('')

        resources = [Resource(resource['resource'], capacity=resource['capacity']) for resource in resources_df.to_dict('records')]

        resource_max_by_project = {}
        for ii, row in resources_df.iterrows():

            if row['max_by_project'] == '':
                max_dict = {}
            else:
                max_dict = eval(row['max_by_project'])

            for k, v in max_dict.items():
                resource_max_by_project.setdefault(k, {})
                resource_max_by_project[k][row['resource']] = v


        return resources, resource_max_by_project

    def _get_project_priorities(self, project_priorities_filepath: str = None):
        columns = {
            'project': str,
            'priority': int
        }
        priorities = self.ui.request_data_from_csv_with_specified_columns(columns, title="Project Priorities", filepath=project_priorities_filepath)
        if priorities is None: return
        priorities = priorities.fillna(10)

        ret = {row['project']: row['priority'] for ii, row in priorities.iterrows()}
        return ret

    def generate_a_gantt(self,
                         task_filepath: str = None,
                         resources_filepath: str = None,
                         project_priorities_filepath: str = None,
                         gantt_name: str = None,
                         ):

        # Get name
        if gantt_name is None:
            gantt_name = self.ui.request_string("Gantt Name:")
        if gantt_name is None: return

        # Get task data
        task_data = self._get_task_data(task_filepath=task_filepath)
        if task_data is None: return

        # Get resources data
        resources, resource_max_by_project = self._get_resource_data(resources_filepath=resources_filepath)

        # Get project priorities
        project_priorities = self._get_project_priorities(project_priorities_filepath=project_priorities_filepath)

        # Build
        self.ui.notify_user(text="Building Gantt...")
        self.gantt = build_and_schedule(gantt_name=gantt_name,
                                        gantt_task_data=task_data.to_dict('records'),
                                        resources=resources,
                                        project_priority=project_priorities,
                                        resource_max_by_project=resource_max_by_project
                                   )

        logging.info(self.gantt)
        self.ui.notify_user("Done building Gantt!")

    def render_an_html(self, html_output_path: str = None, svg_renderings_dir: str = None):
        self.ui.notify_user(text="Rendering HTML...")
        if self.gantt is None or any(self.gantt.activities_not_scheduled):
            self.ui.notify_user("Gantt must be generated before rendering")
            return None

        if html_output_path is None:
            html_output_path = self.ui.request_save_filepath(prompt="Select a path to save the HTML")
        if html_output_path is None: return None

        if svg_renderings_dir is None:
            svg_renderings_dir = self.ui.request_directory(prompt="Select a path to save the .svg files")
        if svg_renderings_dir is None: return None

        build_svgs(self.gantt, output_dirs=[svg_renderings_dir])
        build_html(self.gantt, svg_input_dir=svg_renderings_dir, embed_css=True, output_dirs=[html_output_path])

        self.ui.notify_user(text="Done Rendering HTML!")

    def save_gantt_data(self, out_file: str = None):
        if self.gantt is None:
            self.ui.notify_user(f"Gantt project must be loaded before saving")
            return

        if out_file is None:
            out_file = self.ui.request_save_filepath("Choose a save file path", filetypes=(("CSV", ".csv"),))
        if out_file is None:
            return

        self.ui.notify_user(text=f"Outputting Gantt data to {out_file}")
        df = self.gantt.as_dataframe()
        df.to_csv(out_file, index=None)

    def set_state(self):

        load_state_method = self.ui.request_from_dict(prompt="Load State Method",
                                                    selectionDict={0: "Use config file",
                                                                   1: "Enter manually"})

        if load_state_method == 0:
            self._load_from_config()

        else:
            self.task_filepath = self.ui.request_open_filepath(prompt="Task data filepath", filetypes=(("CSV", ".csv"),))
            if self.task_filepath is None: return None
            self.resources_filepath = self.ui.request_open_filepath(prompt="Resources data filepath", filetypes=(("CSV", ".csv"),))
            if self.resources_filepath is None: return None
            self.project_priorities_filepath = self.ui.request_open_filepath(prompt="Project Priorities Filepath", filetypes=(("CSV", ".csv"),))
            if self.project_priorities_filepath is None: return None
            self.html_output_path = self.ui.request_save_filepath(prompt="Select a path to save the HTML")
            if self.html_output_path is None: return None
            self.svg_renderings_dir = self.ui.request_directory(prompt="Select a path to save the .svg files")
            if self.svg_renderings_dir is None: return None
            self.out_file = self.ui.request_save_filepath("Choose a save file path", filetypes=(("CSV", ".csv"),))
            if self.out_file is None: return None
            self.gantt_name = self.ui.request_string("Gantt Name: ")

        self.ui.notify_user(text=f"State set!")

    def _load_from_config(self):
        if self.config_filepath is None:
            self.config_filepath = self.ui.request_open_filepath(prompt="Select a gantt config.ini file",
                                                                 filetypes=(("CONFIG", ".ini"),))
        config_parser = ConfigParser()
        config_parser.read(self.config_filepath)

        self.task_filepath = config_parser.get('filepaths', 'task_filepath')
        self.resources_filepath = config_parser.get('filepaths', 'resources_filepath')
        self.html_output_path = config_parser.get('filepaths', 'html_output_path')
        self.svg_renderings_dir = config_parser.get('filepaths', 'svg_renderings_dir')
        self.out_file = config_parser.get('filepaths', 'out_file')
        self.project_priorities_filepath = config_parser.get('filepaths', 'project_priority_file')
        self.gantt_name = config_parser.get('meta', 'gantt_name')

    def create_render_and_save(self):

        if self.task_filepath is None or \
           self.resources_filepath is None or \
           self.html_output_path is None or \
           self.svg_renderings_dir is None or \
           self.out_file is None:
            self.ui.notify_user(text="Please set state before running")
            return None

        self.generate_a_gantt(task_filepath=self.task_filepath,
                              resources_filepath=self.resources_filepath,
                              project_priorities_filepath=self.project_priorities_filepath,
                              gantt_name=self.gantt_name)
        self.render_an_html(self.html_output_path, self.svg_renderings_dir)
        self.save_gantt_data(self.out_file)

