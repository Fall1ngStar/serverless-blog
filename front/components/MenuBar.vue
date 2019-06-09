<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <nuxt-link to="/" class="navbar-brand">Serverless blog</nuxt-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse"
            data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup"
            aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
      <div class="navbar-nav">
        <nuxt-link class="nav-item nav-link" to="/post/create">Create post</nuxt-link>
      </div>
    </div>
  </nav>
</template>

<script>
</script>

<style scoped>

</style>
