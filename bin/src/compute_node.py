from src.ssh_spawn_subprocess import ssh_head_spawn_subprocess
import inquirer

def get_active_compute_nodes():
    currently_active = ssh_head_spawn_subprocess(' '.join([
            "sinfo", "-N", "-t", "alloc,mix,idle", '--format=%N,%T,%C,%m', # "--format=%N %T",
            # because of pcluster, filter out nodes which are reserved but not fully started yet
            "| grep -v idle~ | grep -v allocated# | grep -v mixed#"
        ]),
        show_out=False,
        show_cmd=False
    )
    output = currently_active.split('\n')
    nodes = []
    for line in output[1:]:  # Skip the header lines
        if line:  # Skip empty lines
            # fields = line.split()
            node, state, cpus, memory = line.split(',')
            nodes.append({'node': node, 'state': state, 'cpus': cpus, 'memory': memory})
    return nodes


def input_compute_node():
    active_nodes = get_active_compute_nodes()

    node_to_connect = None

    if len(active_nodes) == 1:
        node_to_connect = active_nodes[0]
    else:
        questions = [
            inquirer.List(
                'choice',
                message="select compute node from the list",
                choices=[a_n['node'] for a_n in active_nodes]
            )
        ]

        node_to_connect = inquirer.prompt(questions)

    if node_to_connect == None:
        raise ValueError('no ComputeNode selected')

    node_to_connect = node_to_connect['choice']

    for node in active_nodes:
        if node['node'] == node_to_connect:
            return node

    return 