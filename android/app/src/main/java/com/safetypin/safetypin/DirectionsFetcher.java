package com.safetypin.safetypin;

import android.os.AsyncTask;
import android.util.Log;
import android.widget.TextView;

import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.LatLng;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

/**
 * Created by Ivan on 4/29/2016.
 */
public class DirectionsFetcher extends AsyncTask<Void, Integer, String> {
    private ArrayList<LatLng> locations = new ArrayList<>();
    private GoogleMap mMap;
    private LatLng source;
    private LatLng destination;
    private TextView tv;

    public DirectionsFetcher(GoogleMap mMap,LatLng source, LatLng destination,TextView tv) {
        this.mMap = mMap;
        this.source = source;
        this.destination = destination;
        this.tv = tv;
    }

    protected String doInBackground(Void... voids) {
        String url = makeURL(source,destination);
        String json = getJSONFromURL(url);
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

    protected void onProgressUpdate(Integer... progress) {
    }

    protected void onPostExecute(String result) {
//        clearMarkers();
//        addMarkersToMap(latLngs);
//        tv.setText(result);
        Log.v("JSON RESULT:::",result);
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
        urlString.append("&key=AIzaSyDd6sGcDbxwXKGPm_FQ8p-qW1IDfDZWjpE");
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
}