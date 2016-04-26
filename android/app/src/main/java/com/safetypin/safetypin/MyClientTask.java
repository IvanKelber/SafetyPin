package com.safetypin.safetypin;

import android.os.AsyncTask;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

/**
 * Created by Ivan on 1/21/2016.
 */
public class MyClientTask extends AsyncTask<Void, Void, Void> {
    String dstAddress;
    int dstPort;
    String response;
    TextView textView;
//    FileListView fileListView;
    String message;

    MyClientTask(String addr, int port, TextView textView, String message) {
        dstAddress = addr;
        dstPort = port;
        this.textView = textView;
        this.message = message;
    }

    @Override
    protected Void doInBackground(Void... args) {
        Socket socket = null;
        DataOutputStream dos = null;
        try {
            socket = new Socket(dstAddress,dstPort);
            dos = new DataOutputStream(socket.getOutputStream());
            byte[] b = message.getBytes();
            dos.write(b);

            //read input stream
            DataInputStream dis2 = new DataInputStream(socket.getInputStream());
            InputStreamReader disR2 = new InputStreamReader(dis2);
            BufferedReader br = new BufferedReader(disR2);//create a BufferReader object for input
            StringBuilder sb = new StringBuilder();
            String line;
            while((line = br.readLine()) != null) {
                sb.append(line);
                sb.append("\n");
            }
            response = sb.toString();
            dis2.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(Void result) {
        if(response != null) {
//            String[] fileArray = response.substring(1, response.length() - 2).split(",");
            textView.setText(response);
//            fileListView.setFiles(Arrays.asList(fileArray));
        }
        super.onPostExecute(result);
    }


}
