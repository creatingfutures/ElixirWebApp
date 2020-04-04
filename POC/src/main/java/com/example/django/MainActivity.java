package com.example.django;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {

    private JsonPlaceHolderApi jsonPlaceHolderApi;
    private TextView textViewResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textViewResult = findViewById(R.id.text_view_result);
        Retrofit retrofit = new Retrofit.Builder().
                baseUrl("http://10.0.2.2:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        jsonPlaceHolderApi = retrofit.create(JsonPlaceHolderApi.class);

        Call<List<post>> call = jsonPlaceHolderApi.getPosts(); //put param here

        call.enqueue(new Callback<List<post>>()
        {
            @Override
            public void onResponse(Call<List<post>> call,
                                   Response<List<post>> response)
            {
                if(!response.isSuccessful())
                {
                    textViewResult.setText(response.code());
                    return;
                }
                List<post> posts = response.body();
                for(post post1 : posts)
                {
                    String a = "";
                    a += "ID : "+post1.getId()+"\n";
                    a +=post1.getText()+"\n\n\n";

                    textViewResult.append(a);
                }
            }

            @Override
            public void onFailure(Call<List<post>> call,
                                  Throwable t)
            {
                textViewResult.setText(t.getMessage());
            }
        });

        createPost();
    }

    private void createPost()
    {
        post post = new post(1,"bro");
        Call<post> call = jsonPlaceHolderApi.createPost1(post,1);

        call.enqueue(new Callback<post>()
        {
            @Override
            public void onResponse(Call<post> call,
                                   Response<post> response)
            {
                if(!response.isSuccessful())
                {
                    textViewResult.setText(response.code());
                    return;
                }
                post posts = response.body();

                    String a = ""+response.code()+"\n";
                    a += "ID : "+posts.getId()+"\n";
                    a +=posts.getText()+"\n\n\n";

                    textViewResult.append(a);

            }

            @Override
            public void onFailure(Call<post> call,
                                  Throwable t)
            {
                textViewResult.setText(t.getMessage());
            }
        });
        }
    }




