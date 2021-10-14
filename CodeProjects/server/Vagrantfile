Vagrant.configure(2) do |config|
  config.vm.provider :virtualbox do |v|
        v.name = "dockerExamsServer"
        v.customize [
            "modifyvm", :id,
            "--name", "dockerExamsServer",
            "--memory", 2048,
            "--natdnshostresolver1", "on",
            "--cpus", 2,
        ]
  end

  config.vm.box = "ubuntu/bionic64"
  config.vm.network "forwarded_port", guest: 80, host:8888
  config.vm.network "forwarded_port", guest: 22, host: 55555, id: 'ssh'
  config.vm.network "private_network", ip: "192.168.70.70"
  config.ssh.forward_agent = true
  config.ssh.insert_key = false
  config.vm.synced_folder "../code", "/docker",
    owner: "vagrant",
  	group: "www-data",
  	mount_options: ["dmode=775,fmode=664"]

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.extra_vars = {
        ansible_python_interpreter: "/usr/bin/python3",
    }
  end
end
