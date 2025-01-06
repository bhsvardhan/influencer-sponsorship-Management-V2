<template>
  <div class="container mt-5" style="max-height: 80vh; overflow-y: auto">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="dashboard-title">Sponsor Dashboard</h1>
      <div class="btn-group">
        <router-link to="/sponsor_dashboard" class="btn btn-hover"
          >Profile</router-link
        >
        <br />
        <br />
        <router-link to="/sponsor_dashboard1" class="btn btn-active"
          >Campaigns</router-link
        >
        <br />
        <br />
        <router-link to="/sponsor_dashboard2" class="btn btn-hover"
          >Find</router-link
        >
        <br />
        <br />
        <router-link to="/login" class="btn btn-hover">Logout</router-link>
      </div>
    </div>

    <!-- Welcome Message -->
    <div class="mx-auto text-center">
      <span class="welcome-text">Welcome {{ name }}</span>
    </div>

    <!-- Add Campaign -->
    <div class="text-center mb-4">
      <router-link to="/add_campaign" class="add-campaign-link">
        <h3>Add Campaign</h3>
      </router-link>
    </div>

    <!-- Search Campaigns -->
    <div class="search-bar mb-4">
      <input
        type="text"
        v-model="searchInput"
        @input="searchCampaigns"
        class="form-control search-input"
        placeholder="Search campaigns by name"
      />
    </div>

    <!-- Campaigns -->
    <div class="row" id="campaignsContainer">
      <div
        v-for="(campaign, index) in filteredCampaigns"
        :key="index"
        class="col-md-4"
      >
        <div class="card mb-4 campaign-card">
          <div class="card-body">
            <h5 class="card-title">{{ campaign[0] }}</h5>
            <p class="card-text">{{ campaign[1].substring(0, 100) }}...</p>
            <button
              class="btn btn-primary btn-details"
              @click="viewDetails(campaign)"
            >
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Campaign Details Modal -->
    <div
      class="modal fade"
      tabindex="-1"
      :class="{ show: showModal }"
      style="display: block; background-color: rgba(0, 0, 0, 0.5)"
      v-if="showModal"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Campaign Details</h5>
            <button
              type="button"
              class="close"
              @click="closeModal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p><strong>Name:</strong> {{ selectedCampaign[0] }}</p>
            <p><strong>Description:</strong> {{ selectedCampaign[1] }}</p>
            <p><strong>Start Date:</strong> {{ selectedCampaign[2] }}</p>
            <p><strong>End Date:</strong> {{ selectedCampaign[3] }}</p>
            <p><strong>Budget:</strong> ${{ selectedCampaign[4] }}</p>
            <p><strong>Visibility:</strong> {{ selectedCampaign[5] }}</p>
            <p><strong>Goals:</strong> {{ selectedCampaign[6] }}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "", // Sponsor's name
      campaigns: [], // List of campaigns
      searchInput: "", // Input for search functionality
      showModal: false, // Modal visibility state
      selectedCampaign: [], // Currently selected campaign for details
    };
  },
  computed: {
    filteredCampaigns() {
      if (this.searchInput.trim() === "") {
        return this.campaigns;
      }
      return this.campaigns.filter((campaign) =>
        campaign[0].toLowerCase().includes(this.searchInput.toLowerCase())
      );
    },
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await axios.get(
          "http://localhost:5000/sponsor_dashboard1"
        );
        this.name = localStorage.getItem("username");
        this.campaigns = response.data.campaigns;
      } catch (error) {
        console.error(
          "Error fetching dashboard data:",
          error.response?.data || error.message
        );
      }
    },
    async searchCampaigns() {
      try {
        const response = await axios.get(
          `http://localhost:5000/search_campaigns?search=${encodeURIComponent(
            this.searchInput
          )}`
        );
        this.campaigns = response.data;
      } catch (error) {
        console.error(
          "Error searching campaigns:",
          error.response?.data || error.message
        );
      }
    },
    viewDetails(campaign) {
      this.selectedCampaign = campaign;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedCampaign = [];
    },
  },
  async created() {
    await this.fetchDashboardData();
  },
};
</script>

<style scoped>
/* General Layout */
.dashboard-title {
  font-size: 2.5rem;
  color: #343a40;
  font-weight: 600;
}

.welcome-text {
  font-size: 2rem;
  font-weight: bold;
  color: #495057;
  margin-bottom: 1rem;
}

/* Modal */
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1050;
}

.modal-dialog {
  max-width: 500px;
  margin: auto;
}

.modal-content {
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e9ecef;
  padding: 1rem 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e9ecef;
  text-align: right;
}

.close {
  background: none;
  border: none;
  font-size: 1.5rem;
}
</style>
