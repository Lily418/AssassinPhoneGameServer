using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class SynchronousSocketClient {

    volatile bool callConnected = false;
    byte[] bytes = new byte[1024];
    Socket sender;

    public SynchronousSocketClient(){
        StartClient();
        Thread t = new Thread(new ThreadStart(CheckCallStatus));
        t.Start();
    }

    private void StartClient() {
        // Data buffer for incoming data.


        // Connect to a remote device.
        try {
            // Establish the remote endpoint for the socket.
            // This example uses port 11000 on the local computer.
            IPEndPoint remoteEP = new IPEndPoint(IPAddress.Parse("178.62.27.159"), 3500);

            // Create a TCP/IP  socket.
            sender = new Socket(AddressFamily.InterNetwork,
            SocketType.Stream, ProtocolType.Tcp );

            // Connect the socket to the remote endpoint. Catch any errors.
            try {
                sender.Connect(remoteEP);

                Console.WriteLine("Socket connected to {0}",
                sender.RemoteEndPoint.ToString());


            } catch (ArgumentNullException ane) {
                Console.WriteLine("ArgumentNullException : {0}",ane.ToString());
            } catch (SocketException se) {
                Console.WriteLine("SocketException : {0}",se.ToString());
            } catch (Exception e) {
                Console.WriteLine("Unexpected exception : {0}", e.ToString());
            }

        } catch (Exception e) {
            Console.WriteLine( e.ToString());
        }
    }

    private void CheckCallStatus(){
        int bytesRec;
        while(true){
            while((bytesRec = sender.Receive(bytes)) > 0)
            {
                string message = Encoding.ASCII.GetString(bytes,0,bytesRec);
                Console.WriteLine(message);
                if(message == "ringing")
                {
                    callConnected = true;
                }
                else if(message == "completed")
                {
                    callConnected = false;
                }
            }
        }
    }

    public bool getCallStatus(){
        return callConnected;
    }

    public static int Main(String[] args) {
        SynchronousSocketClient ssc = new SynchronousSocketClient();
        while(true)
        {
            Console.WriteLine(ssc.getCallStatus());
        }
    }
}
