<template>
  <div class="container">
    <post-card v-for="post in posts" :post="post" v-bind:key="post.post_id"/>
    <div class="button-toolbar">
      <div class="btn-group mr-2">
        <nuxt-link
          v-for="page in pages"
          v-bind:key="page.content"
          :class="page.classes"
          :to="page.url"
        >{{page.content}}
        </nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
  import PostCard from '~/components/PostCard.vue';

  export default {
    components: {PostCard},
    async asyncData({params, query, env}) {
      let url = `${env.apiUrl}/posts/${query.page ? '?page=' + query.page : ''}`;
      let response = await fetch(url);
      let data = await response.json();
      return {
        posts: data.posts,
        pages: data.pages
      };
    },
    watchQuery: ['page'],
    key: to => to.fullPath
  };
</script>

<style>
  .button-toolbar {
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>

