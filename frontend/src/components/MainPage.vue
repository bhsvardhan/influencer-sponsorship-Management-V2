<template>
  <div class="min-vh-100 bg-light">
    <!-- Hero Section -->
    <div class="hero-section d-flex flex-column align-items-center justify-content-center text-center text-light px-4">
      <h1 class="display-3 fw-bold mb-3">Influencer Engagement & Sponsorship System</h1>
      <p class="fs-5 mb-4">
        Connect Sponsors and Influencers. Advertise your products/services, and let influencers monetize their influence.
      </p>
      <button 
        class="btn btn-primary btn-lg px-4 py-2 shadow"
        @click="this.$router.push('/login')">
        Sign In to Continue
      </button>
    </div>

    <!-- Features Section -->
    <div class="features-section py-5">
      <div class="container">
        <h2 class="text-center fw-bold mb-5">Key Features</h2>
        <div class="row g-4">
          <div 
            class="col-lg-4 col-md-6"
            v-for="feature in features"
            :key="feature.title">
            <div class="feature-card bg-white shadow-sm p-4 h-100 rounded">
              <h5 class="fw-bold mb-3 text-primary">{{ feature.title }}</h5>
              <p class="text-secondary mb-0">{{ feature.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Section -->
    <div class="footer-section py-4 text-center text-light">
      <p class="mb-0">
        © 2024 Influencer Sponsorship System. All Rights Reserved.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      features: [
        {
          title: "User-Friendly Interface",
          desc: "Navigate through a clean and intuitive interface that simplifies influencer-sponsorship management tasks.",
        },
        {
          title: "Efficient Workflow",
          desc: "Streamline collaboration between influencers and sponsors with effective tools for project management.",
        },
        {
          title: "Data-Driven Insights",
          desc: "Make informed decisions using analytics that showcase the impact of your campaigns and partnerships.",
        },
      ],
    };
  },
};
</script>

<style scoped>
/* Hero Section Styling */
.hero-section {
  background: linear-gradient(to right, #4e54c8, #8f94fb);
  min-height: 50vh;
  padding: 3rem 1rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* Features Section */
.features-section {
  background: #f8f9fa;
}
.feature-card {
  border: 1px solid #ddd;
  transition: transform 0.3s, box-shadow 0.3s;
}
.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* Footer Section */
.footer-section {
  background: #343a40;
  color: #d3d3d3;
}
</style>
