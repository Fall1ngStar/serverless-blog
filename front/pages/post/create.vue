<template>
  <div class="container">
    <h3>Create an article</h3>
    <form @submit="createPost" id="create-post">
      <div class="form-group">
        <label for="title">Title</label>
        <input class="form-control" name="title" type="text" v-model="title">
      </div>
      <div class="form-group">
        <label for="content">Content</label>
        <textarea class="form-control" name="content" rows="13" v-model="content"/>
      </div>
      <div class="form-group">
        <label for="Author">Author</label>
        <input class="form-control" name="author" type="text" v-model="author">
      </div>
      <button class="btn btn-primary" type="submit">Submit article</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "create",
  methods: {
    async createPost(e) {
      e.preventDefault();
      let body = {
        title: this.title,
        author: this.author,
        content: this.content
      };
      let url = process.env.apiUrl + "/posts/create";
      let params = {
          method: 'POST',
          cors: true,
          body: JSON.stringify(body)
      };
      let response = await fetch(url, params);
      let content = await response.json();
      this.$router.push('/post/' + content.post_id);
    }
  },
  data: () => {
    return {
      title: "",
      content: "",
      author: ""
    };
  }
};
</script>

<style scoped>
.container {
  padding: 0.5em;
}
</style>