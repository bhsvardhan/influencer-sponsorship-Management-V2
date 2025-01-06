<template>
  <div class="admin-dashboard">
    <nav class="nav-bar">
      <span
        class="nav-item"
        :class="{ active: currentTab === 'Info' }"
        @click="currentTab = 'Info'"
        >Info</span
      >
      <span
        class="nav-item"
        :class="{ active: currentTab === 'Find' }"
        @click="$router.push('/admin_dashboard1')"
        >Find</span
      >
      <span
        class="nav-item"
        :class="{ active: currentTab === 'Stats' }"
        @click="$router.push('/stats')"
        >Stats</span
      >
      <span class="nav-item" @click="$router.push('/login')">Logout</span>
    </nav>

    <div class="content">
      <h2>Welcome, Admin</h2>

      <div v-if="currentTab === 'Info'" class="info-section">
        <div class="campaigns-section">
          <h3>Ongoing Campaigns:</h3>
          <div v-if="loading.campaigns">Loading campaigns...</div>
          <div v-else>
            <div v-if="campaigns.length > 0" class="campaigns-list">
              <div
                v-for="campaign in campaigns"
                :key="campaign.name"
                class="campaign-item"
              >
                <div class="campaign-header">
                  <strong>{{ campaign.name }}</strong>
                </div>
                <div class="campaign-details">
                  <p>{{ campaign.description }}</p>
                  <p>Start: {{ formatDate(campaign.start_date) }}</p>
                  <p>End: {{ formatDate(campaign.end_date) }}</p>
                  <p>Budget: {{ campaign.budget }}</p>
                  <p>Visibility: {{ campaign.visibility }}</p>
                  <p>Goals: {{ campaign.goals }}</p>
                  <button @click="viewCampaign(campaign)" class="view-btn">
                    View Details
                  </button>
                </div>
              </div>
            </div>
            <p v-else>No ongoing campaigns found.</p>
          </div>
        </div>

        <div class="flagged-section">
          <h3>Flagged Users/Campaigns:</h3>
          <div v-if="loading.flagged">Loading flagged items...</div>
          <div v-else>
            <div v-if="flaggedItems.length > 0" class="flagged-list">
              <div
                v-for="flagged in flaggedItems"
                :key="flagged.name"
                class="flagged-item"
              >
                <div class="flagged-header">
                  <span>{{ flagged.name }}</span>
                  <span class="flagged-type">({{ flagged.type }})</span>
                </div>
                <div class="flagged-details">
                  <p>Flagged on: {{ formatDate(flagged.flag_date) }}</p>
                  <div class="flagged-actions">
                    <button @click="viewFlagged(flagged)" class="view-btn">
                      View
                    </button>
                    <button
                      @click="removeFlagged(flagged.name)"
                      class="remove-btn"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <p v-else>No flagged users or campaigns found.</p>
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
      currentTab: "Info",
      campaigns: [],
      flaggedItems: [],
      loading: {
        campaigns: false,
        flagged: false,
      },
      error: {
        campaigns: null,
        flagged: null,
      },
    };
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return "N/A";
      const options = { year: "numeric", month: "short", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    async fetchCampaigns() {
      this.loading.campaigns = true;
      try {
        const response = await axios.get(
          "http://localhost:5000/current_campaigns"
        );
        console.log("Campaigns response:", response.data); // Debug log
        this.campaigns = Array.isArray(response.data) ? response.data : [];
      } catch (error) {
        console.error("Error fetching campaigns:", error);
        this.error.campaigns = error.message;
      } finally {
        this.loading.campaigns = false;
      }
    },
    async fetchFlaggedUsersCampaigns() {
      this.loading.flagged = true;
      try {
        const response = await axios.get(
          "http://localhost:5000/flagged_users_campaigns"
        );
        console.log("Flagged items response:", response.data); // Debug log
        this.flaggedItems = Array.isArray(response.data) ? response.data : [];
      } catch (error) {
        console.error("Error fetching flagged items:", error);
        this.error.flagged = error.message;
      } finally {
        this.loading.flagged = false;
      }
    },
    async logout() {
      try {
        await axios.post("http://localhost:5000/logout");
        this.$router.push("/login");
      } catch (error) {
        console.error("Logout error:", error);
      }
    },
    viewCampaign(campaign) {
      alert(JSON.stringify(campaign, null, 2));
    },
    viewFlagged(flagged) {
      alert(JSON.stringify(flagged, null, 2));
    },
    async removeFlagged(name) {
      try {
        await axios.delete(`http://localhost:5000/remove_flagged/${name}`);
        this.flaggedItems = this.flaggedItems.filter(
          (item) => item.name !== name
        );
      } catch (error) {
        console.error("Error removing flagged item:", error);
        alert("Failed to remove flagged item");
      }
    },
  },
  mounted() {
    this.fetchCampaigns();
    this.fetchFlaggedUsersCampaigns();
  },
};
</script>

<style>
.nav-bar {
  display: flex;
  gap: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 5px;
}

.nav-item {
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-item.active {
  background-color: #add8e6;
  font-weight: bold;
}

.content {
  margin-top: 20px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.campaigns-list,
.flagged-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.campaign-item,
.flagged-item {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
  background-color: white;
}

.campaign-header,
.flagged-header {
  margin-bottom: 10px;
  font-size: 1.1em;
}

.flagged-type {
  color: #666;
  margin-left: 8px;
}

.campaign-details,
.flagged-details {
  font-size: 0.9em;
}

.flagged-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

button {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.view-btn {
  background-color: #4caf50;
  color: white;
}

.remove-btn {
  background-color: #f44336;
  color: white;
}

button:hover {
  opacity: 0.9;
}
</style>
