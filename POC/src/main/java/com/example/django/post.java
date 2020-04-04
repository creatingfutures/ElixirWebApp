package com.example.django;

import com.google.gson.annotations.SerializedName;

public class post {

    //private int userId;

    @SerializedName("emp_id")
    private int id;

    //private String title;

    @SerializedName("firstname")
    private String text;

   // public int getuserId() {
   //     return userId;
   // }


    public post(int id, String text) {
        this.id = id;
        this.text = text;
    }

    public int getId() {
        return id;
    }

  //  public String getTitle() {
   //     return title;
    //}

    public String getText() {
        return text;
    }
}
