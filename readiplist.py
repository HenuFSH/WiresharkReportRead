import os

class Node(object):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
        self.sub_dict={}

    def insert_sub_node(self, value) -> "Node":
        if not self.sub_dict.__contains__(value):
            self.sub_dict[value] = Node(value)
        return self.sub_dict[value]

    def display(self):
        print(self.value, end=',')
        for sub_node in self.sub_dict.values():
            sub_node.display()

class Root(Node):
    def __init__(self, root) -> None:
        super().__init__(root)

    def display(self):
        for sub_value in self.sub_dict.values():
            sub_value.display()
            print()

def read_ip_list(filename) -> Root:
    root = Root('')
    with open(filename, 'r') as f:
        ip=''
        protocol=''
        port=''
        for line in f.readlines():
            if len(line) > 3:
                value = str.split(line.strip() , ' ')[0]
                if line[0] == ' ' and line[1] != ' ':
                    ip=value
                elif line[0] == ' ' and line[1] == ' ' and line[2] != ' ':
                    protocol = value
                elif line[0] == ' ' and line[1] == ' ' and line[2] == ' ' and line[3] != ' ':
                    port=value
                    root.insert_sub_node(ip).insert_sub_node(protocol).insert_sub_node(port)
    return root

def ip_port_diff(root1:Root, root2:Root) -> Root:
    new_root = root1
    for ip in list(root1.sub_dict.keys()):
        # 判断root1的ip不在root2中
        if root2.sub_dict.__contains__(ip):
            del new_root.sub_dict[ip]

    return new_root

def ip_port_merge(root1:Root, root2:Root) -> Root:
    new_root = root1
    for ip in root2.sub_dict.values():
        for protocol in ip.sub_dict.values():
            for port in protocol.sub_dict.values():
                new_root.insert_sub_node(ip.value).insert_sub_node(protocol.value).insert_sub_node(port.value)

    return new_root

def read_ip_list_dir(path) -> Root:
    root = Root('')
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            filename = os.path.join(path, file)
            root = ip_port_merge(root, read_ip_list(filename))
    else:
        print('Path not exist: ' + path)
    return root

if __name__ == '__main__':
    root1 = read_ip_list_dir("./qmt/")
    root2 = read_ip_list_dir("./sys")

    root3 = ip_port_diff(root1, root2)
    root3.display()
    # root1.display()
    # root2.display()

