#!/usr/bin/env python
from src.cluster_status import show_cluster_status_progress

try: 
    show_cluster_status_progress()
except Exception as e:
    print(f"An error occurred:")
    print(e)
    print(e.output)