testinfra_hosts = ['ansible://bind-host']


def test_openvpnclient(host):
    cmd = host.run("systemctl list-units --all openvpn*")
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0
    assert 'client@lan' in cmd.stdout
