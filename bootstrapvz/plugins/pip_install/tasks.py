from bootstrapvz.base import Task
from bootstrapvz.common import phases
from bootstrapvz.common.tasks import apt
from bootstrapvz.common.tasks import network


class AddPipPackage(Task):
	description = 'Adding `pip\' to the image packages'
	phase = phases.preparation
	predecessors = [apt.AddDefaultSources]

	@classmethod
	def run(cls, info):
		info.packages.add('python-pip')


class PipInstallCommand(Task):
	description = 'Install python packages from pypi with pip'
	phase = phases.system_modification
	successors = [network.RemoveHostname, network.RemoveDNSInfo]

	@classmethod
	def run(cls, info):
		from bootstrapvz.common.tools import log_check_call
		packages = info.manifest.plugins['pip_install']['packages']
		pip_install_command = ['chroot', info.root, 'pip', 'install']
		pip_install_command.extend(packages)
		log_check_call(pip_install_command)
