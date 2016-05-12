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
import java.util.HashMap;
import java.util.LinkedHashMap;

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
    final HashMap<Integer,String> CRIME_TYPES = new HashMap<>();
    final HashMap<Integer,Float> CRIME_COLORS = new HashMap<>();

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
        this.message = "(" + convertToString(source) + "," + convertToString(destination) + ")";

        CRIME_TYPES.put(0,"Homicide");
        CRIME_TYPES.put(1,"Sexual Assault");
        CRIME_TYPES.put(2,"Robbery");
        CRIME_TYPES.put(3,"Assault");
        CRIME_TYPES.put(4,"Burglary");
        CRIME_TYPES.put(5,"Theft");
        CRIME_TYPES.put(6,"Battery");
        CRIME_TYPES.put(7,"Weapons Violation");
        CRIME_TYPES.put(8,"Offense Involving Children");
        CRIME_TYPES.put(9,"Sexual Offense");
        CRIME_TYPES.put(10,"Hate Crime");

        CRIME_COLORS.put(0,BitmapDescriptorFactory.HUE_RED);
        CRIME_COLORS.put(1,BitmapDescriptorFactory.HUE_ORANGE);
        CRIME_COLORS.put(2,BitmapDescriptorFactory.HUE_GREEN);
        CRIME_COLORS.put(3,BitmapDescriptorFactory.HUE_YELLOW);
        CRIME_COLORS.put(4,BitmapDescriptorFactory.HUE_MAGENTA);
        CRIME_COLORS.put(5,BitmapDescriptorFactory.HUE_ROSE);
        CRIME_COLORS.put(6,BitmapDescriptorFactory.HUE_BLUE);
        //The rest aren't used in NYC
        CRIME_COLORS.put(7,BitmapDescriptorFactory.HUE_RED);
        CRIME_COLORS.put(8,BitmapDescriptorFactory.HUE_RED);
        CRIME_COLORS.put(9,BitmapDescriptorFactory.HUE_RED);
        CRIME_COLORS.put(10,BitmapDescriptorFactory.HUE_RED);

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
            socket = new Socket(dstAddress, dstPort);
            dos = new DataOutputStream(socket.getOutputStream());
            byte[] b = message.getBytes();
            dos.write(b);

            //read input stream
            DataInputStream dis2 = new DataInputStream(socket.getInputStream());
            InputStreamReader disR2 = new InputStreamReader(dis2);
            BufferedReader br = new BufferedReader(disR2);//create a BufferReader object for input
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
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
        if (response != null) {
//            String[] fileArray = response.substring(1, response.length() - 2).split(",");
//            textView.setText(response);
            Log.v("RECEIVED RESPONSE:", response);
            ArrayList<LinkedHashMap<LatLng,Integer>> coords = parseResponse(response);
            ArrayList<LatLng> waypoints = new ArrayList<>(coords.get(0).keySet());
            Log.e("WAYPOINTS:", waypoints.toString() + "" + waypoints.size());
            if (waypoints.isEmpty()) {
                Log.e("RECEIVED RESPONSE '[]'", response);
                listener.onEmptyReponse();
            }
            waypoints.add(0, source);
            waypoints.add(destination);

//            LatLng l = new LatLng(Double.parseDouble(latlng[0]),Double.parseDouble(latlng[1]));
//            Marker m = mMap.addMarker(new MarkerOptions().position(l).title("Destination").draggable(true));
            ArrayList<ArrayList<LatLng>> segments = new ArrayList<>();
            segments.add(new ArrayList<LatLng>());

            for (int i = 0; i < waypoints.size(); i++) {
                if (i != 0 && i % 22 == 0) {
                    segments.get(segments.size() - 1).add(waypoints.get(i));
                    segments.add(new ArrayList<LatLng>());
                }
                segments.get(segments.size() - 1).add(waypoints.get(i));
            }
            for (ArrayList wp : segments) {
                DirectionsFetcher df = new DirectionsFetcher(mMap, (LatLng) wp.get(0), (LatLng) wp.get(wp.size() - 1), wp);
                df.execute();
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
//            fileListView.setFiles(Arrays.asList(fileArray));
            for (LatLng point : waypoints) {
                mMap.addMarker(new MarkerOptions().position(point).title("Intersection in Path")
                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)));
            }

            for (LatLng crime : coords.get(1).keySet()) {
                Integer type = coords.get(1).get(crime);
                crimes.add(mMap.addMarker(new MarkerOptions().position(crime).title(CRIME_TYPES.get(type))
                        .icon(BitmapDescriptorFactory.defaultMarker(CRIME_COLORS.get(type))).visible(false)));
            }
        }
        super.onPostExecute(result);
    }

    private ArrayList<LinkedHashMap<LatLng,Integer>> parseResponse(String r) {
        ArrayList<LinkedHashMap<LatLng,Integer>> ret = new ArrayList<>();
        ret.add(new LinkedHashMap<LatLng,Integer>());
        ret.add(new LinkedHashMap<LatLng,Integer>());
        try {
            String k = r.substring(2, r.length() - 2);
            String regex = "\\), ";

            String[] coords = k.split("\\], \\[");
            Log.e("WAYPOINTS:", coords[0]);
            Log.e("CRIMES:", coords[1]);

            String[] points = coords[0].split(regex);
            for (String s : points) {
                if (!s.contains(")")) {
                    s += ")";
                }
                Double lat = Double.parseDouble(s.substring(1, s.indexOf(",")));
                Double lng = Double.parseDouble(s.substring(s.indexOf(",") + 2, s.length() - 2));
                ret.get(0).put(new LatLng(lat, lng),0);
            }


            String[] crimeInfo = coords[1].split(regex);
            for (String s : crimeInfo) {
                if (!s.contains(")")) {
                    s += ")";
                }
                int type = Integer.parseInt(s.substring(1,s.indexOf(',')));
                Double lat = Double.parseDouble(s.substring(ordinalIndexOf(s,',',0) + 2, ordinalIndexOf(s,',',1)));
                Double lng = Double.parseDouble(s.substring(ordinalIndexOf(s,',',1) + 2, s.length() - 2));
                ret.get(1).put(new LatLng(lat, lng),type);
            }
        } catch (StringIndexOutOfBoundsException e) {
            return ret;
        }

        return ret;
    }


    public int ordinalIndexOf(String str, char c, int n) {
        int pos = str.indexOf(c, 0);
        while (n-- > 0 && pos != -1)
            pos = str.indexOf(c, pos + 1);
        return pos;
    }
}
