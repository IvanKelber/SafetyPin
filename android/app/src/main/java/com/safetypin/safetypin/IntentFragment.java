package com.safetypin.safetypin;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.DialogFragment;
import android.view.LayoutInflater;
import android.view.View;

import com.google.android.gms.maps.model.LatLng;

/**
 * This is a fragment that appears when the server fails to calculate the data
 * either due to missing data or locations that are out of bounds.
 */
public class IntentFragment extends DialogFragment {


    private LatLng destination;
    @NonNull
    @Override
    /*
    * This creates the popup dialog box containing the number picker.
    * The layout inflater was used to inflate the custom view difficulty_picker_fragmentment.xml
    * which is just a centered number picker.
    * Clicking play will create the intent and pass whatever integer is currently selected
    * to GameActivity.*/
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        Bundle b = getArguments();
        destination = new LatLng(b.getDouble("lat"),b.getDouble("lng"));
        LayoutInflater layoutInflater = (LayoutInflater) getActivity().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View view = layoutInflater.inflate(R.layout.intent_fragment, null);
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        builder.setTitle("Oops!")
                .setMessage("Looks like we are missing some relevant data in that path.  " +
                            "Your safest bet may be Uber or Google Maps")
                .setView(view)
                .setPositiveButton("Google Maps", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {

                            String uriString = "google.navigation:q=";
                            uriString += ""+destination.latitude;
                            uriString += "," + destination.longitude;
                            Uri gmmIntentUri = Uri.parse(uriString);
                            Intent mapIntent = new Intent(Intent.ACTION_VIEW, gmmIntentUri);
                            mapIntent.setPackage("com.google.android.apps.maps");
                            startActivity(mapIntent);
                        }
                    }

                )
                .setNegativeButton("Uber", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            try {
                                PackageManager pm = getActivity().getPackageManager();
                                pm.getPackageInfo("com.ubercab", PackageManager.GET_ACTIVITIES);
                                String uri =
                                        "uber://?action=setPickup&pickup=my_location&client_id=YOUR_CLIENT_ID";
                                Intent intent = new Intent(Intent.ACTION_VIEW);
                                intent.setData(Uri.parse(uri));
                                startActivity(intent);
                            } catch (PackageManager.NameNotFoundException e) {
                                // No Uber app! Open mobile website.
                                String url = "https://m.uber.com/sign-up?client_id=YOUR_CLIENT_ID";
                                Intent intent = new Intent(Intent.ACTION_VIEW);
                                intent.setData(Uri.parse(url));
                                startActivity(intent);
                            }
                                }
                            }

                    );
                    return builder.create();
                }
    }