<template>
  <div class="container mt-5">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Admin Dashboard</h1>
      <div class="btn-group">
        <router-link to="/admin_dashboard" class="btn btn-hover">Info</router-link>
        <router-link to="/admin_dashboard1" class="btn btn-hover">Find</router-link>
        <router-link to="/stats" class="btn btn-info">Stats</router-link>
        <router-link to="/logOut" class="btn btn-hover">Logout</router-link>
      </div>
    </div>

    <!-- Welcome Message -->
    <div class="mx-auto">
      <span class="display-2">Welcome {{ name }}</span>
    </div>

    <h1 class="mb-4">Statistics</h1>

    <!-- Statistics Cards -->
    <div class="row">
      <div class="col-md-4">
        <div class="card bg-primary text-white mb-4">
          <div class="card-header">Total Campaigns</div>
          <div class="card-body">
            <h5 class="card-title">{{ stats.total_campaigns }}</h5>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-success text-white mb-4">
          <div class="card-header">Total Influencers</div>
          <div class="card-body">
            <h5 class="card-title">{{ stats.total_influencers }}</h5>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-info text-white mb-4">
          <div class="card-header">Total Sponsors</div>
          <div class="card-body">
            <h5 class="card-title">{{ stats.total_sponsors }}</h5>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="card bg-warning text-white mb-4">
          <div class="card-header">Total Budget</div>
          <div class="card-body">
            <h5 class="card-title">{{ stats.total_budget }}</h5>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card bg-danger text-white mb-4">
          <div class="card-header">Total Requests</div>
          <div class="card-body">
            <h5 class="card-title">Total: {{ stats.total_requests }}</h5>
            <h5 class="card-title">Accepted: {{ stats.total_accepted_requests }}</h5>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="row mt-4">
      <div class="col-md-6">
        <canvas id="userStatsChart"></canvas>
      </div>
      <div class="col-md-6">
        <canvas id="requestsStatsChart"></canvas>
      </div>
    </div>

    <div class="row mt-4">
      <div class="col-md-12">
        <canvas id="budgetChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from "chart.js";
import axios from "axios";

export default {
  data() {
    return {
      name: "", // Admin's name
      stats: {
        total_campaigns: 0,
        total_influencers: 0,
        total_sponsors: 0,
        total_budget: 0,
        total_requests: 0,
        total_accepted_requests: 0,
      },
    };
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get("http://localhost:5000/api/stats");
        this.stats = response.data;
        console.log("Stats:", this.stats); // Debugging log
        this.renderCharts();
      } catch (error) {
        console.error(
          "Error fetching stats:",
          error.response?.data || error.message
        );
      }
    },
    renderCharts() {
      // Check for canvas elements
      if (!document.getElementById("userStatsChart")) {
        console.error("Canvas element for userStatsChart not found");
        return;
      }

      // Chart for campaigns, influencers, and sponsors
      new Chart(document.getElementById("userStatsChart"), {
        type: "pie",
        data: {
          labels: ["Campaigns", "Influencers", "Sponsors"],
          datasets: [
            {
              data: [
                this.stats.total_campaigns,
                this.stats.total_influencers,
                this.stats.total_sponsors,
              ],
              backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
            },
          ],
        },
      });

      // Chart for total requests and accepted requests
      new Chart(document.getElementById("requestsStatsChart"), {
        type: "bar",
        data: {
          labels: ["Total Requests", "Accepted Requests"],
          datasets: [
            {
              data: [
                this.stats.total_requests,
                this.stats.total_accepted_requests,
              ],
              backgroundColor: ["#4BC0C0", "#FF9F40"],
            },
          ],
        },
      });

      // Chart for total budget
      new Chart(document.getElementById("budgetChart"), {
        type: "doughnut",
        data: {
          labels: ["Budget"],
          datasets: [
            {
              data: [this.stats.total_budget],
              backgroundColor: ["#9966FF"],
            },
          ],
        },
      });

      console.log("Charts rendered successfully");
    },
  },
  async created() {
    // Fetch stats when the component is created
    await this.fetchStats();
  },
};
</script>

<style scoped>
.card-title {
  font-size: 1.5rem;
}
canvas {
  max-width: 100%;
  margin: 0 auto;
}
</style>
