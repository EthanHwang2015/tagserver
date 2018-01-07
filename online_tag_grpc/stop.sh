ps ux| grep suiyi_tag_server.py | grep -v "grep"| awk '{print $2}' | xargs kill -9
