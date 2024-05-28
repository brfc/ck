import click
import yaml
import json
import os
import textwrap

# cheetsheat compose
# [ 
#       { 
#           Topic: 
#           commands : [(command_line , description), ...]
#       } 
#       , ...
# ]

class cs:
    def __init__(self):
        with open("conf.yaml", 'r') as f:
            dict = yaml.safe_load(f)
            self.fpath = dict["database"]

        self.fdict = self.check(self.fpath);

    def check(self, fpath):
        if not os.path.exists(fpath):
            with open(fpath, 'w') as file:
                print("[CS] new db file at " + fpath)
        with open(fpath, 'r') as file:
            data = json.load(file)
        return data

    def plist(self, l):
        for item in l:
            print("\t" + str(item['cmd']) + '\n' )
            if item['description']:
                print("\t\033[4mDESCRIPTION:\033[0m")
                description = textwrap.fill(str(item['description']), width=40)
                print("".join(["\n\t" + line for line in description.split("\n")]))
            print("\t---")
            print("")

    def la(self):
        """
        List all commands
        """
        cl = []
        for t in self.fdict:
            if (t["commands"] == []):
                continue
            print("\033[;1m" + t["Topic"] + ":\033[0m")
            self.plist(t["commands"])

    def lt(self):
        """
        List all topics
        """
        cl = []
        for t in self.fdict:
            print('\t' + t["Topic"])
        
    def ltool(self):
        """
        List all tools
        """
        cl = []
        for t in self.fdict:
            for c in t["commands"]:
                # remove repeated cmds
                if c["tool"] not in cl:
                    cl.append(c["tool"])
        for c in cl:
            print('\t' + c)

    def command_obj(self, cmd, description=None):
        tool = cmd.split()[0]
        description = "" if None else description
        obj = { "tool": tool , "cmd": cmd, "description": description}
        return obj
    
    def topic_obj(self, topic, cmd, description):
        obj = {"Topic": topic, "commands": [self.command_obj(cmd,description)]}
        return obj

    def dump(self):
        with open(self.fpath, 'w') as f:
            json.dump(self.fdict, f, indent=4)
        print(self.fpath + " updated ")


    def k(self, topic, cmd, description):
        for item in self.fdict:
            if item["Topic"] == topic:
                cmd_obj = self.command_obj(cmd, description)
                item["commands"].append(self.command_obj(cmd, description))
                self.dump()
                return     
        self.fdict.append( self.topic_obj(topic, cmd, description))
        self.dump()
        

    
## Client line options
@click.group()
def scl():
    pass

@click.command(help="Save the following command with [--description]")
@click.argument('cmd')
@click.option('--topic', "--t", required=True, help='command topic')
@click.option('--description', "--d", help='command description')
def keep(cmd, topic, description):
    sheet = cs()
    sheet.k(topic, cmd, description)

@click.command(help="List sheetcheat commands")
@click.option('--topic','--t', is_flag=True, help='list of topics in db')
@click.option('--tool', is_flag=True, help='list of tools in db')
def list(topic, tool):
    sheet = cs()
    if tool:
        sheet.ltool()
    elif topic:
        sheet.lt()
    else:
        sheet.la()

scl.add_command(keep)
scl.add_command(list)



if __name__ == '__main__':
    scl()
