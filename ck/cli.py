import click
import yaml
import json
import os
import textwrap

CONFIG_FILE = "/Users/brfc/workspace/ck/conf.yaml"


class CheatSheet:
    def __init__(self):
        self.fpath = self._load_config()

    def _load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
        return config["database"]

    def _create_db_file_if_not_exists(self):
        if not os.path.exists(self.fpath):
            with open(self.fpath, 'w'):
                pass  # Create an empty file
            print("[CS] New database \
                file created at", self.fpath)

    def _read_commands_from_db(self):
        with open(self.fpath, 'r') as file:
            return json.load(file)

    def _save_commands_to_db(self, data):
        with open(self.fpath, 'w') as f:
            json.dump(data, f, indent=4)
        print("Database updated:", self.fpath)

    def list_commands(self, commands):
        for item in commands:
            print("\t" + item['cmd'] + '\n' )
            description = \
                textwrap.fill(
                    str(item.get('description', '')), 
                    width=40
                )
            print("\t\033[4mDESCRIPTION:\033[0m")
            print("".join(["\n\t" + \
                line for line in description.split("\n")]))
            print("\t---\n")

    def list_all(self):
        data = self._read_commands_from_db()
        for item in data:
            if item["commands"]:
                print("\033[;1m" + \
                    item["Topic"] + ":\033[0m")
                self.list_commands(item["commands"])

    def list_topics(self):
        data = self._read_commands_from_db()
        for item in data:
            print('\t' + item["Topic"])

    def list_tools(self):
        data = self._read_commands_from_db()
        tools = set()
        for item in data:
            for cmd in item["commands"]:
                tools.add(cmd["tool"])
        for tool in sorted(tools):
            print('\t' + tool)

    def add_command(self, topic, cmd, description):
        data = self._read_commands_from_db()
        for item in data:
            if item["Topic"] == topic:
                item["commands"].append(\
                    {
                    "tool": cmd.split()[0], \
                    "cmd": cmd, "description": description
                    })
                self._save_commands_to_db(data)
                return
        data.append(\
            {"Topic": topic, "commands": \
                [{"tool": cmd.split()[0], 
                "cmd": cmd, "description": description}
            ]})
        self._save_commands_to_db(data)


## CLI Commands
@click.group()
def cli():
    pass

@click.command(help="Save the following command with [--description]")
@click.argument('cmd')
@click.option('--topic', "--t", required=True, help='Command topic')
@click.option('--description', "--d", help='Command description')
def keep(cmd, topic, description):
    cheat_sheet = CheatSheet()
    cheat_sheet.add_command(topic, cmd, description)

@click.command(help="List cheat sheet commands")
@click.option('--topic', '--t', is_flag=True, help='List topics')
@click.option('--tool', is_flag=True, help='List tools')
def list(topic, tool):
    cheat_sheet = CheatSheet()
    if tool:
        cheat_sheet.list_tools()
    elif topic:
        cheat_sheet.list_topics()
    else:
        cheat_sheet.list_all()


cli.add_command(keep)
cli.add_command(list)

if __name__ == '__main__':
    cli()
