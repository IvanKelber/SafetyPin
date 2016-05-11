package com.safetypin.safetypin;

import android.graphics.Color;
import android.os.AsyncTask;
import android.util.Log;

import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Polyline;
import com.google.android.gms.maps.model.PolylineOptions;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Ivan on 4/29/2016.
 */
public class DirectionsFetcher extends AsyncTask<LatLng, String, String> {
    private ArrayList<LatLng> locations = new ArrayList<>();
    private GoogleMap mMap;
    private LatLng source;
    private LatLng destination;
    private ArrayList<LatLng> waypoints;
//    private TextView tv;

    public DirectionsFetcher(GoogleMap mMap,LatLng source, LatLng destination,ArrayList<LatLng> waypoints) {
        this.mMap = mMap;
        this.source = source;
        this.destination = destination;
        this.waypoints = waypoints;
//        this.tv = tv;
    }

    protected String doInBackground(LatLng... latLngs) {
        String url = makeURL(source,destination);
        String json = getJSONFromURL(url);
//        publishProgress(json);
        return json;

//
//            HttpRequest request = requestFactory.buildGetRequest(url);
//            HttpResponse httpResponse = request.execute();
//            DirectionsResult directionsResult = httpResponse.parseAs(DirectionsResult.class);
//            String encodedPoints = directionsResult.routes.get(0).overviewPolyLine.points;
//            latLngs = PolyUtil.decode(encodedPoints);
//        } catch (Exception ex) {
//            ex.printStackTrace();
//        }
//        return null;
    }

    protected void onProgressUpdate(String... progress) {
        super.onProgressUpdate(progress);
        drawPath(progress[0]);

    }

    protected void onPostExecute(String result) {
//        clearMarkers();
//        addMarkersToMap(latLngs);
//        tv.setText(result);
        Log.v("JSON RESULT:::",result);
        //draw the poly path
        drawPath(result);
    }

    private String makeURL (LatLng source, LatLng destination) {
        StringBuilder urlString = new StringBuilder();
        urlString.append("https://maps.googleapis.com/maps/api/directions/json");
        urlString.append("?origin=");
        urlString.append(""+source.latitude);
        urlString.append(",");
        urlString.append(""+source.longitude);
        urlString.append("&destination=");
        urlString.append(""+destination.latitude);
        urlString.append(",");
        urlString.append(""+destination.longitude);
        urlString.append("&sensor=false&mode=walking&alternatives=false&region=us");
        urlString.append("&waypoints=optimize:true:");
        String poly = parseWaypoints(waypoints);
        Log.e("POLYLINE:",poly);
        urlString.append(poly);
        urlString.append("&key=AIzaSyDd6sGcDbxwXKGPm_FQ8p-qW1IDfDZWjpE");
        Log.e("Total URL:",urlString.toString());
        return urlString.toString();
    }

    public String getJSONFromURL(String urlstring) {
        StringBuilder json = new StringBuilder();
        try {
            URL url = new URL(urlstring);
            HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
            try {
                InputStream in = new BufferedInputStream(httpURLConnection.getInputStream());
                BufferedReader reader = new BufferedReader(new InputStreamReader(in));
                String line;
                while((line = reader.readLine()) != null) {
                    json.append(line).append('\n');
                }
            } finally {
                httpURLConnection.disconnect();
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return json.toString();
    }

    public void drawPath(String result) {
        try {
            //Tranform the string into a json object
            final JSONObject json = new JSONObject(result);
            JSONArray routeArray = json.getJSONArray("routes");
            JSONObject routes = routeArray.getJSONObject(0);
            JSONObject overviewPolylines = routes.getJSONObject("overview_polyline");
            String encodedString = overviewPolylines.getString("points");
            List<LatLng> list = decodePoly(encodedString);
            Polyline line = mMap.addPolyline(new PolylineOptions()
                            .addAll(list)
                            .width(12)
                            .color(Color.parseColor("#05b1fb"))//Google maps blue color
                            .geodesic(true)
            );
           /*
           for(int z = 0; z<list.size()-1;z++){
                LatLng src= list.get(z);
                LatLng dest= list.get(z+1);
                Polyline line = mMap.addPolyline(new PolylineOptions()
                .add(new LatLng(src.latitude, src.longitude), new LatLng(dest.latitude,   dest.longitude))
                .width(2)
                .color(Color.BLUE).geodesic(true));
            }
           */
        }
        catch (JSONException e) {

        }
    }


    private List<LatLng> decodePoly(String encoded) {

        List<LatLng> poly = new ArrayList<LatLng>();
        int index = 0, len = encoded.length();
        int lat = 0, lng = 0;

        while (index < len) {
            int b, shift = 0, result = 0;
            do {
                b = encoded.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            int dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lat += dlat;

            shift = 0;
            result = 0;
            do {
                b = encoded.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            int dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lng += dlng;

            LatLng p = new LatLng( (((double) lat / 1E5)),
                    (((double) lng / 1E5) ));
            poly.add(p);
        }

        return poly;
    }

    private String parseWaypoints(ArrayList<LatLng> latlngs) {
        StringBuilder parser = new StringBuilder();
        for (LatLng l : latlngs) {
            parser.append(l.latitude +","+ l.longitude +"|");
        }
        String parsed = parser.toString();
        if(parsed.length() < 2) {
            Log.e("PARSED < 2:",latlngs.toString());
            return parsed;
        }
        parsed = parsed.substring(0,parsed.length()-2);
//        return PolyUtil.encode(latlngs);
        return parsed;
    }
}