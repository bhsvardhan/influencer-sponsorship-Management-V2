<template>
  <div class="container mt-5" style="max-height: 80vh; overflow-y: auto;">
    <div class="dashboard-header d-flex justify-content-between align-items-center mb-4 p-3 rounded shadow">
      <h1 class="text-primary">Sponsor Dashboard</h1>
      <div class="btn-group">
        <router-link to="/sponsor_dashboard" class="btn btn-info">Profile</router-link>
        <br>
        <router-link to="/sponsor_dashboard1" class="btn btn-primary">Campaigns</router-link>
        <br>
        <router-link to="/sponsor_dashboard2" class="btn btn-success">Find</router-link>
        <br>
        <router-link to="/login" class="btn btn-danger">Logout</router-link>
      </div>
    </div>

    <div class="welcome-section text-center my-5">
      <h2 class="display-4 text-secondary">Welcome, {{ userName }}!</h2>
    </div>

    <section>
      <h2 class="mb-3 text-secondary">Active Campaigns</h2>
      <div class="row">
        <div v-for="campaign in campaigns" :key="campaign.id" class="col-md-12 mb-3">
          <div class="card shadow-sm">
            <div class="card-body d-flex justify-content-between align-items-center">
              <div>
                <h5 class="card-title text-primary">{{ campaign.name }}</h5>
                <div class="progress" style="height: 20px;">
                  <div
                    class="progress-bar bg-success"
                    :style="{ width: calculateProgress(campaign.start_date, campaign.end_date) + '%' }"
                    role="progressbar"
                    :aria-valuenow="calculateProgress(campaign.start_date, campaign.end_date)"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  >
                    {{ calculateProgress(campaign.start_date, campaign.end_date).toFixed(2) }}%
                  </div>
                </div>
              </div>
              <button @click="viewCampaign(campaign.name)" class="btn btn-primary">View Details</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="mt-5">
      <h2 class="mb-3 text-secondary">New Requests</h2>
      <div id="requestsContainer" class="row">
        <div v-for="request in requests" :key="`${request.campaign_name}-${request.influencer_username}`" class="col-md-12 mb-3">
          <div class="card shadow-sm">
            <div class="card-body d-flex justify-content-between align-items-center">
              <div>
                <h5 class="card-title text-primary">{{ request.campaign_name }} - {{ request.influencer_username }}</h5>
                <p><strong>Messages:</strong> {{ request.messages }}</p>
                <p><strong>Requirements:</strong> {{ request.requirements }}</p>
                <p><strong>Payment Amount:</strong> ${{ request.payment_amount }}</p>
                <p><strong>Status:</strong> {{ request.status }}</p>
              </div>
              <div>
                <button @click="viewCampaign(request.campaign_name)" class="btn btn-info me-2">View Campaign</button>
                <button @click="acceptRequest(request.campaign_name, request.influencer_username)" class="btn btn-success me-2">Accept</button>
                <button @click="rejectRequest(request.campaign_name, request.influencer_username)" class="btn btn-danger">Reject</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userName: "",
      campaigns: [],
      requests: [],
      campaignInfo: {},
    };
  },
  methods: {
    fetchDashboardData() {
      axios.get("http://localhost:5000/api/sponsor_dashboard").then((response) => {
        this.campaigns = response.data.campaigns;
        this.userName = localStorage.getItem("username");
      });
    },
    fetchRequests() {
      axios.get("http://localhost:5000/api/view_requests").then((response) => {
        if (response.data.requests) {
          this.requests = response.data.requests;
        }
      });
    },
    calculateProgress(startDate, endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      const today = new Date();

      const totalDuration = (end - start) / (1000 * 60 * 60 * 24);
      const elapsedDuration = (today - start) / (1000 * 60 * 60 * 24);

      return Math.max(0, Math.min((elapsedDuration / totalDuration) * 100, 100));
    },
    viewCampaign(campaignName) {
      axios
        .post("http://localhost:5000/current_campaigns", { campaign_name: campaignName })
        .then((response) => {
          if (response.data.campaign_info) {
            this.campaignInfo = response.data.campaign_info;
            this.$bvModal.show("campaignInfoModal");
          } else {
            alert("Campaign not found.");
          }
        });
    },
    acceptRequest(campaignName, influencerUsername) {
      axios
        .post("http://localhost:5000/api/accept_request", {
          campaign_name: campaignName,
          influencer_username: influencerUsername,
        })
        .then(() => {
          alert("Request accepted successfully!");
          this.fetchRequests();
        })
        .catch(() => {
          alert("Failed to accept request.");
        });

    },
    rejectRequest(campaignName, influencerUsername) {
      axios
        .post("http://localhost:5000/api/reject_request", {
          campaign_name: campaignName,
          influencer_username: influencerUsername,
        })
        .then(() => {
          alert("Request rejected successfully!");
          this.fetchRequests();
        })
        .catch(() => {
          alert("Failed to reject request.");
        });
    },
  },
  mounted() {
    this.fetchDashboardData();
    this.fetchRequests();
  },
};
</script>

<style scoped>
.dashboard-header {
  background-color: #f8f9fa;
}

.card {
  border: none;
}

.card-title {
  font-weight: bold;
}

.progress-bar {
  font-size: 14px;
  line-height: 20px;
}

h2 {
  font-size: 1.75rem;
}
</style>
