# Submission to hackathons

To run on Mac OS:
`python3 main.py --num_workers 2 --nhands 2 --net_type mb1-ssd --model_path models/mb1-ssd-Epoch-95-Loss-1.3421423047780991.pth --display 1`

Python requirements:
pytorch, keyboard, cv2

To run distributed framework:
On server machine run 
`python3 recv_images.py --model_path models/mb1-ssd-Epoch-95-Loss-1.3421423047780991.pth`

And on the client (Macbook) run
`python3 main_distributed.py --display 1`
