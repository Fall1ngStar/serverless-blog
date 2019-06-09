<template>
  <div class="card">
    <h5 class="card-header">{{post.title}}</h5>
    <div class="card-body">
      <h6 class="card-title">By {{post.author}}</h6>
      <p class="card-text"> {{post.content.split(' ').slice(0, 10).reduce((acc, curr) => acc + " " +
        curr) + "..."}}</p>
      <p class="card-text"><em>{{new Date(post.create_date).toLocaleString()}}</em></p>
      <nuxt-link class="btn btn-primary" :to="'/post/' + post.post_id">Go to article</nuxt-link>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'PostCard',
    props: ['post'],
  }
</script>

<style scoped>
  .card {
    margin: 1em;
  }
</style>
