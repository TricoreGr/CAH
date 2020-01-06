<script>
export default {
  mounted() {
    localStorage.removeItem("authToken");
    this.$router.push("/");
  }
};
</script>
