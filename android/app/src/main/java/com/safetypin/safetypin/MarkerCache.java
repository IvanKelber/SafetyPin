package com.safetypin.safetypin;

import com.google.android.gms.maps.model.Marker;

import java.util.LinkedList;

/**
 * Created by Ivan on 4/28/2016.
 */
public class MarkerCache<E> extends LinkedList<E> {

    private int limit;

   public MarkerCache(int limit) {
       this.limit = limit;
   }

    @Override
    public boolean add(E o) {
        if (o.getClass() == Marker.class) {
            super.add(o);
            while(this.size() > limit) {
                Marker m = (Marker) super.remove();
                m.remove();
            }
            return true;
        }
        return false;
    }
}
