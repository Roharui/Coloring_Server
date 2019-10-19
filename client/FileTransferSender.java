import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
 
public class FileTransferSender {
    public static final int DEFAULT_BUFFER_SIZE = 1024;
    private final String serverIP = "127.0.0.1"; 
    private final int port = 8080;

    private File getFile(String fileName)
    {
        File file = new File(fileName);
        if (!file.exists()) {
            System.out.println("File not Exist.");
            System.exit(0);
        }

        return file;
    }

    private void sendImg(String cmd, File file)
    {
        long fileSize = file.length();
        long totalReadBytes = 0;
        byte[] buffer = new byte[DEFAULT_BUFFER_SIZE];
        int readBytes;
        double startTime = 0;
        
        byte[] input_buffer = new byte[100];
         
        try {
            FileInputStream fis = new FileInputStream(file);
            Socket socket = new Socket(this.serverIP, this.port);
            if(!socket.isConnected()){
                System.out.println("Socket Connect Error.");
                System.exit(0);
            }
            
            startTime = System.currentTimeMillis();
            OutputStream os = socket.getOutputStream();
            InputStream is = socket.getInputStream();
            
            os.write(cmd.getBytes());
            is.read(input_buffer);
            
            while ((readBytes = fis.read(buffer)) > 0) {
                os.write(buffer, 0, readBytes);
                totalReadBytes += readBytes;
                System.out.println("In progress: " + totalReadBytes + "/"
                        + fileSize + " Byte(s) ("
                        + (totalReadBytes * 100 / fileSize) + " %)");
            }
            
            os.write("done".getBytes());
            
            System.out.println("File transfer completed.");
            fis.close();
            os.close();
            socket.close();
        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
         
        double endTime = System.currentTimeMillis();
        double diffTime = (endTime - startTime)/ 1000;;
        double transferSpeed = (fileSize / 1000)/ diffTime;
         
        System.out.println("time: " + diffTime+ " second(s)");
        System.out.println("Average transfer speed: " + transferSpeed + " KB/s");
    }

    private File mkImg(String name)
    {
        File file = null;
        try{
            file = new File(name) ;
            FileWriter fw = new FileWriter(file, true) ;
            fw.flush();
            fw.close();
        }catch(Exception e){
            e.printStackTrace();
        }
        return file;
    }

    private void getImg(File file)
    {
        double startTime = 0;
        byte[] input_buffer = new byte[DEFAULT_BUFFER_SIZE];

        try {
            FileOutputStream fos = new FileOutputStream(file);
            Socket socket = new Socket(this.serverIP, this.port);
            if(!socket.isConnected()){
                System.out.println("Socket Connect Error.");
                System.exit(0);
            }
            
            startTime = System.currentTimeMillis();
            OutputStream os = socket.getOutputStream();
            InputStream is = socket.getInputStream();
            
            os.write("IGET".getBytes());
            is.read(input_buffer);
            os.write("done".getBytes());
            
            is.read(input_buffer);
            while(input_buffer.toString() != "done"){
                fos.write(input_buffer);
                os.write(" ".getBytes());
                is.read(input_buffer);
            }
            
            System.out.println("File rescive completed.");
            fos.close();
            os.close();
            socket.close();
        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
         
        double endTime = System.currentTimeMillis();
        double diffTime = (endTime - startTime)/ 1000;;
         
        System.out.println("time: " + diffTime+ " second(s)");
    }

    public static void main(String[] args) {
        String FileName = 
        		"C:\\Users\\user\\Downloads\\test.jpeg";              //String FileName = "test.mp4";
        FileTransferSender ft = new FileTransferSender();
        //File file = ft.getFile(FileName);
        //ft.sendImg("ISEND", file);
        File file = ft.mkImg("test.jpeg");
        ft.getImg(file);
    }
}