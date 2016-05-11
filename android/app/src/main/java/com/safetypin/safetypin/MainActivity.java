package com.safetypin.safetypin;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;


public class MainActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final EditText addr = (EditText) findViewById(R.id.addr_text);
        final TextView response = (TextView) findViewById(R.id.text_view);
        final Button button = (Button) findViewById(R.id.toMaps);

        addr.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView textView, int actionId, KeyEvent keyEvent) {
                boolean handled = false;
                if (actionId == EditorInfo.IME_ACTION_SEND) {
//                    String[] addressInfo = addr.getText().toString().split(":");
//                    MyClientTask mct = new MyClientTask(addressInfo[0],Integer.parseInt(addressInfo[1]),response,"I come in peace.");
//                    mct.execute();
                    handled = true;
                }
                return handled;
            }
        });

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(MainActivity.this,MapsActivity.class);
                i.putExtra("address",addr.getText().toString());
                startActivity(i);
            }
        });

        button.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                Uri gmmIntentUri = Uri.parse("google.navigation:q=Brown+University,Providence");
                Intent mapIntent = new Intent(Intent.ACTION_VIEW, gmmIntentUri);
                mapIntent.setPackage("com.google.android.apps.maps");
                startActivity(mapIntent);
//                try {
//                    PackageManager pm = getApplicationContext().getPackageManager();
//                    pm.getPackageInfo("com.ubercab", PackageManager.GET_ACTIVITIES);
//                    String uri =
//                            "uber://?action=setPickup&pickup=my_location&client_id=YOUR_CLIENT_ID";
//                    Intent intent = new Intent(Intent.ACTION_VIEW);
//                    intent.setData(Uri.parse(uri));
//                    startActivity(intent);
//                } catch (PackageManager.NameNotFoundException e) {
//                    // No Uber app! Open mobile website.
//                    String url = "https://m.uber.com/sign-up?client_id=YOUR_CLIENT_ID";
//                    Intent i = new Intent(Intent.ACTION_VIEW);
//                    i.setData(Uri.parse(url));
//                    startActivity(i);
//                }
                return true;
            }
        });
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
