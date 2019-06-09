<template>
  <div class="container">
    <div class="card" id="post">
      <h1 class="card-header">{{post.title}}</h1>
      <div class="card-body">
        <p class="card-title">{{post.content}}</p>
        <h5 class="card-text">Posted by {{post.author}}</h5>
        <h6 class="card-text">{{new Date(post.create_date).toLocaleString()}}</h6>
      </div>
      <button class="btn btn-danger" id="delete-button" v-on:click="deletePost">Delete post</button>
    </div>
    <div class="container" id="delete-post"></div>
    <form @submit="sendComment" id="comment-form">
      <div class="form-group">
        <input class="form-control" type="text" name="comment" v-model="comment_content">
      </div>
      <button class="btn btn-primary" type="submit">Submit comment</button>
    </form>
    <div v-if="post.comments.length > 0" class="container">
      <h4>Comments</h4>
      <ul class="list-group">
        <li
          class="list-group-item"
          v-for="comment in post.comments"
          v-bind:key="comment.create_date"
        >{{comment.content}}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "id",
  async asyncData({ params, env }) {
    let url = env.apiUrl + "/posts/" + params.id;
    let response = await fetch(url);
    let data = await response.json();
    return {
      post: data
    };
  },
  methods: {
    async deletePost({ params, env }) {
      let url = process.env.apiUrl + "/posts/" + this.$route.params.id;
      console.log(url);
      let response = await fetch(url, { method: "DELETE" });
      this.$router.push("/");
    },
    async sendComment(e) {
      e.preventDefault();
      let url = process.env.apiUrl + "/posts/" + this.$route.params.id;
      let params = {
        method: "POST",
        cors: true,
        body: JSON.stringify({
          content: this.comment_content
        })
      };
      let response = await fetch(url, params);
      this.post.comments.unshift({ content: this.comment_content });
      this.comment_content = "";
      console.log(await response.json());
    }
  },
  data: () => {
    return {
      comment_content: ""
    };
  }
};
</script>

<style scoped>
#post,
#comment-form {
  margin: 1em;
}
#delete-post {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
