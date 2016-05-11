package com.safetypin.safetypin;

import android.os.AsyncTask;
import android.util.Log;

import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
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
    GoogleMap mMap;
    private String message;
    private LatLng source;
    private LatLng destination;
    OnEmptyResponseListener listener;
    private ArrayList<Marker> crimes;

    public interface OnEmptyResponseListener {
        public void onEmptyReponse();
    }

    public void setOnEmptyResponseListener(OnEmptyResponseListener listener) {
        this.listener = listener;
    }

    MyClientTask(String addr, int port, GoogleMap mMap, LatLng source, LatLng destination, ArrayList<Marker> crimes) {
        dstAddress = addr;
        dstPort = port;
//        this.textView = textView;
        this.crimes = crimes;
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
            Log.v("RECEIVED RESPONSE:",response);
            ArrayList<ArrayList<LatLng>> coords = parseResponse(response);
            ArrayList<LatLng> waypoints = coords.get(0);
            Log.e("WAYPOINTS:",waypoints.toString() + "" + waypoints.size());
            if (waypoints.isEmpty()) {
                Log.e("RECEIVED RESPONSE '[]'",response);
                listener.onEmptyReponse();
            }
            waypoints.add(0, source);
            waypoints.add(destination);

//            LatLng l = new LatLng(Double.parseDouble(latlng[0]),Double.parseDouble(latlng[1]));
//            Marker m = mMap.addMarker(new MarkerOptions().position(l).title("Destination").draggable(true));
            ArrayList<ArrayList<LatLng>> segments = new ArrayList<ArrayList<LatLng>>();
            segments.add(new ArrayList<LatLng>());

            for (int i = 0; i < waypoints.size(); i++) {
                    if (i != 0 && i % 22 == 0) {
                        segments.get(segments.size() - 1).add(waypoints.get(i));
                        segments.add(new ArrayList<LatLng>());
                    }
                segments.get(segments.size() - 1).add(waypoints.get(i));
            }
            for (ArrayList wp : segments) {
                DirectionsFetcher df = new DirectionsFetcher(mMap,(LatLng)wp.get(0),(LatLng)wp.get(wp.size()-1),wp);
                df.execute();
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
//            fileListView.setFiles(Arrays.asList(fileArray));
            for (LatLng point : waypoints) {
                mMap.addMarker(new MarkerOptions().position(point)
                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)));
            }

            for (LatLng point : coords.get(1)) {
                crimes.add(mMap.addMarker(new MarkerOptions().position(point)
                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED)).visible(false)));
            }
        }
        super.onPostExecute(result);
    }

    private ArrayList<ArrayList<LatLng>> parseResponse(String r) {
        String k = r.substring(2,r.length()-2);
        Log.e("SPLIT STRING:",k);
        String regex = "\\), ";
        ArrayList<ArrayList<LatLng>> ret = new ArrayList<>();
        ret.add(new ArrayList<LatLng>());
        ret.add(new ArrayList<LatLng>());
        String[] coords = k.split("\\], \\[");
        Log.e("WAYPOINTS:",coords[0]);
        Log.e("CRIMES:",coords[1]);

        for (int i = 0; i < 2; i++) {
            String[] splits = coords[i].split(regex);
            for (String s : splits) {
                try {
                    if (!s.contains(")")) {
                        s += ")";
                    }
                    Double lat = Double.parseDouble(s.substring(1, s.indexOf(",")));
                    Double lng = Double.parseDouble(s.substring(s.indexOf(",") + 2, s.length() - 2));
                    ret.get(i).add(new LatLng(lat, lng));
                } catch (StringIndexOutOfBoundsException e) {
                    Log.e("STRING INDEX OOB:", s);
                }
            }

        }
        return ret;
    }
}
