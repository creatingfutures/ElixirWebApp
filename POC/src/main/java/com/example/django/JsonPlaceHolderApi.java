package com.example.django;

import java.util.List;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;

public interface JsonPlaceHolderApi {

    @GET("employee1")
    Call<List<post>> getPosts();

   // @GET("emoloyee1/{id}/name")
    //Call<List<post>> getPosts(@Path(id) int postId);

    //Call<List<post>> getPosts(@Query("userId") int userId);

    @POST("employee3")
    Call<post> createPost(@Body post post);

    @PUT("employee2/{id}")
    Call<post> createPost1(@Body post post,@Path("id") int emp_id);
}
