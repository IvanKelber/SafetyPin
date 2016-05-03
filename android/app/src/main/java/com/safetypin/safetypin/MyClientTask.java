package com.safetypin.safetypin;

import android.os.AsyncTask;
import android.util.Log;

import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.ArrayList;

/**
 * Created by Ivan on 1/21/2016.
 */
public class MyClientTask extends AsyncTask<Void, Void, Void> {
    String dstAddress;
    int dstPort;
    String response;
//    TextView textView;
    GoogleMap mMap;
//    FileListView fileListView;
    private String message;
    private LatLng source;
    private LatLng destination;

    MyClientTask(String addr, int port, GoogleMap mMap, LatLng source, LatLng destination) {
        dstAddress = addr;
        dstPort = port;
//        this.textView = textView;
        this.message = message;
        this.mMap = mMap;
        this.source = source;
        this.destination = destination;
        this.message = "("+convertToString(source) + "," + convertToString(destination)+")";
    }

    private String convertToString(LatLng l) {
        double lat = l.latitude;
        double lng = l.longitude;
        return "(" + lat + "," + lng + ")";
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
//            textView.setText(response);
            ArrayList<LatLng> waypoints =parseResponse(response);


//            LatLng l = new LatLng(Double.parseDouble(latlng[0]),Double.parseDouble(latlng[1]));
//            Marker m = mMap.addMarker(new MarkerOptions().position(l).title("Destination").draggable(true));

            DirectionsFetcher df = new DirectionsFetcher(mMap,source,destination,waypoints);
            df.execute();
//            fileListView.setFiles(Arrays.asList(fileArray));
            for (LatLng point : waypoints) {
                mMap.addMarker(new MarkerOptions().position(point));
            }
        }
        super.onPostExecute(result);
    }

    private ArrayList<LatLng> parseResponse(String r) {
        String k = r.substring(1,r.length()-2);
        Log.e("SPLIT STRING:",k);
        String regex = "\\), ";
        ArrayList<LatLng> ret = new ArrayList<LatLng>();
        String[] splits = k.split(regex);
        for (String s : splits) {
            s += ")";
            Double lat = Double.parseDouble(s.substring(1,s.indexOf(",")));
            Double lng = Double.parseDouble(s.substring(s.indexOf(",")+2,s.length()-2));
            ret.add(new LatLng(lat,lng));

        }
        return ret;
    }
}
