from src.ssh_spawn_subprocess import ssh_head_spawn_subprocess

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
