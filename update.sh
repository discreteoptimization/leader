PATH=$PATH:/home/ec2-user/bin/R-2.12.1/bin

cd /home/ec2-user/leader/001/
./makeIt.py
./makePoints.py 
./postIt.py
