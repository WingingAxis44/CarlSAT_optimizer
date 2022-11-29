#!/bin/bash
#Automated script for build docker image, volume and starting container
#Values for Docker image, volume and container variables should be kept the same
#because other script files use these exact names to refer to the same image, container
#and volume.

dockerimage=dimage
container=mysql-db
volume=mysql-vol-cap
sql_pword=pw
database=hyperopt

#Flag variables
wcard=''
timeout=2
interactive='false'
updateLocalDB='false'
freshImage='false'
testRepo='false'
wcardPath="wcards/rnd/tests/"

#Help message if the user misuses the script.
print_usage() {
	printf "\nUSAGE:
./autorun.sh [options]\n
OPTIONS:
-z : ARG\tProblem wcard, no default value. Must be specified if -i flag not passed. Just give the file name (don't specify the path)
-t : ARG\tTimeout for CarlSAT, default = 2. Should be specified along with -z flag.
-h\t\tDisplay this help message
-i\t\tEnable run container interactively, default = false. Must be specified if not passing -z and -t flag.
-u\t\tUpdate local hyperopt database with gitLab synched sqlscripts/hyperopt.sql DB, default = false
-f\t\tRemove associated docker image and rebuild from scratch. i.e. docker image is purged\n
NOTE:
The -i flag is mutually exclusive from the -z and -t flags. The -i flag will not directly call the Wrapper class
as interactive mode is intended for development and debugging. If -i is not passed, the docker container will run as a Daemon
and call the Wrapper class directly with relevant output being printed to host console. If passing the -i flag, an interactive bash terminal will be spawned for the user
within the Docker container.
The flags -u and -f can be combined with both interactive and non-interactive mode.\n 
EXAMPLES:
./autorun.sh -z test1.wcard -t 2 -f -u
./autorun.sh -i -u\n"
}

container_exists(){
	sudo docker ps -a --format '{{.Names}}' | grep -Eq "^${container}\$"
}

#If the user doesn't pass any options.
if [ $# -eq 0 ]; then
   print_usage
   exit 1
fi



while getopts :z:t:ifruy flag; do
	case "${flag}" in
    	z) wcard=${OPTARG}
    		;;
    	t) timeout=${OPTARG}
    		;;
		i) interactive='true'
			;;
		f) freshImage='true'
			;;
		u) updateLocalDB='true'
			;;
		r) testRepo='true'
			;;
		h) print_usage
			;;
    	*) echo -e "Invalid option: -${flag}"
			print_usage
			exit 1
			;;
	esac
done

#Checks if the user tried to run with interactive mode enabled as well as specified a wcard.
#Wcard will just be ignored, but worthwhile notifiying the user as such

if [ "$testRepo" == 'false' ] ; then

	if ( [ "$interactive" == 'true' ] ) && ( [ -n "$wcard" ] ) ; then
	echo -e "NOTE: Script called with interactive flag AND having specified a wcard --> Wcard flag ignored.\n"
	fi

#Checks if the user tried to run in non-interactive mode, but didn't specify a problem card.
#This is a problem and the execution must terminate

	if ( [ "$interactive" == 'false' ] ) && ( [ -z "$wcard" ] ) ; then
	print_usage
	echo -e "\n\e[1;31mUSAGE ERROR: If not running in interactive mode, please specify -w wcard\e[0m\n"
	exit 1
	fi

fi



if [ "$freshImage" == 'true' ] ; then
	echo -e "Fresh Image requested. Removing image ${dockerimage}\n"
	if container_exists ; then
		sudo docker stop $container >/dev/null
    	sudo docker rm $container >/dev/null
	fi
	sudo docker image rm $dockerimage >/dev/null
	echo -e "${dockerimage} Removed\n"
fi

sudo docker build -t $dockerimage .


#Check to see if the docker volume exists. If it doesn't create it, otherwise do nothing.
if ( !(sudo docker volume ls -q | grep -q $volume >/dev/null) ) ; then
	docker volume create $volume >/dev/null
	echo -e "\e[1;36mCreated docker volume:\e[0m ${volume}\n"
	
else
	echo -e "\e[1;36mUsing docker volume:\e[0m ${volume}"	
fi

#Checks to see if the mysql container has already been created. If it is, then it needs to be stopped and removed before restarting it.
if container_exists ; then
#if sudo docker ps -a --format '{{.Names}}' | grep -Fq $container ; then
        echo -e "\e[1;36mContainer <${container}> already exists. Stopping and removing it first.\e[0m\n"
        sudo docker stop $container >/dev/null
        sudo docker rm $container >/dev/null

fi



#The port number stuff might need to be changed (could cause an error if the client has a container running on that port.
echo -e "\e[1;36mStarting docker container:\e[0m" $container

sudo docker run -d -p 3306:3306 \
--name=$container \
-v $volume:/var/lib/mysql \
--mount type=tmpfs,destination=/mnt/ramdisk \
-e MYSQL_ROOT_PASSWORD=$sql_pword \
$dockerimage

echo -e "\e[1;36mContainer started \e[0m\n"

if [ $updateLocalDB == 'true' ] ; then
	echo -ne "\e[1;36mUpdate local DB specified"
	sleep 1
	echo -ne "."
	sleep 1
	echo -ne "."
	sleep 1
	echo -ne ".\e[0m\n"
	sleep 1
	sudo docker exec -i $container sh -c 'exec mysql -uroot -ppw hyperopt' <./sqlscripts/hyperopt.sql
	echo -e "\e[1;36mHyperopt database in docker container has been restored\nfrom hyperopt.sql database stored in sqlscripts.\e[0m\n"
fi

if [ "$testRepo" == 'false' ] ; then

	if [ $interactive == 'true' ] ; then
	echo -e "\e[1;32mExecuting interactive container with bash terminal\n 
If you haven't yet already, please see README.md file for steps on how to run our program.
It is available in this current directory (type more README.md)\n\n\e[0m"

	
	sudo docker exec -it $container bash

	else
	echo -e "\e[1;32mExecuting Hyper-parameter optimization program with input problem: ${wcard} and timeout: ${timeout} seconds\e[0m\n"

	
	#Might want to add feature to generate a new wcard if the user wants that. Otherwise just go fetch one from the tests directory
	wcardPath+="${wcard}"
	
	
	sudo docker exec -i $container sh -c "python3 -u src/wrapper.py ${wcardPath} ${timeout}"
	fi

else

echo -ne "\e[1;32mTesting "
sleep 1
echo -ne "."
sleep 1
echo -ne "."
sleep 1
echo -ne ".\e[0m\n"
sleep 1
sudo docker exec -i $container sh -c "python3 -u src/RepoTester.py"

fi


