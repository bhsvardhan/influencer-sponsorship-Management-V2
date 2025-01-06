<template>
  <div class="container mt-5" style="max-height: 80vh; overflow-y: auto;">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Sponsor Dashboard</h1>
      <div class="btn-group">
        <router-link to="/sponsor_dashboard" class="btn btn-hover">Profile</router-link>
        <br>
        <router-link to="/sponsor_dashboard1" class="btn btn-hover">Campaigns</router-link>
        <br>
        <router-link to="/sponsor_dashboard2" class="btn btn-info">Find</router-link>
        <br>
        <router-link to="/login" class="btn btn-hover">Logout</router-link>
      </div>
    </div>
    <div class="mx-auto">
      <span class="display-2">Welcome {{ name }}</span>
    </div>

    <div class="form-group">
      <input
        type="text"
        v-model="query"
        class="form-control"
        placeholder="Search campaigns or influencers"
        @input="search"
      />
    </div>

    <table class="table mt-4">
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="results.length === 0">
          <td colspan="3">No results found.</td>
        </tr>
        <tr v-for="(item, index) in results" :key="index">
          <td>{{ item.name }}</td>
          <td>{{ item.type }}</td>
          <td>
            <button
              v-if="item.type === 'campaign'"
              @click="viewCampaign(item.id)"
              class="btn btn-info btn-sm"
            >
              View
            </button>
            <button
              v-if="item.type === 'influencer'"
              @click="viewInfluencer(item.id)"
              class="btn btn-info btn-sm"
            >
              View
            </button>
            <button
              v-if="item.type === 'influencer'"
              @click="sendRequestForm(item.id)"
              class="btn btn-primary btn-sm"
            >
              Request
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal for viewing details -->
    <div v-if="showDetailsModal" class="modal-overlay">
      <div class="modal">
        <h2>{{ modalTitle }}</h2>
        <div v-html="modalContent"></div>
        <button @click="closeModal" class="btn btn-secondary">Close</button>
      </div>
    </div>

    <!-- Modal for sending requests -->
    <div v-if="showRequestModal" class="modal-overlay">
      <div class="modal">
        <h2>Send Request</h2>
        <form @submit.prevent="submitRequest">
          <div class="form-group">
            <label for="campaign_name">Campaign Name:</label>
            <input type="text" v-model="requestForm.campaign_name" class="form-control" required />
          </div>
          <div class="form-group">
            <label for="message">Message:</label>
            <textarea v-model="requestForm.message" class="form-control" required></textarea>
          </div>
          <div class="form-group">
            <label for="requirements">Requirements:</label>
            <textarea v-model="requestForm.requirements" class="form-control" required></textarea>
          </div>
          <div class="form-group">
            <label for="payment_amount">Payment Amount:</label>
            <input type="number" v-model="requestForm.payment_amount" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" @click="closeModal" class="btn btn-secondary">Close</button>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      name: "", // This will be fetched from localStorage
      query: "",
      results: [],
      showDetailsModal: false,
      showRequestModal: false,
      modalTitle: "",
      modalContent: "",
      requestForm: {
        campaign_name: "",
        message: "",
        requirements: "",
        payment_amount: "",
        influencerId: "",
        sponsorUsername: "", // Adding sponsorUsername to the request
      },
    };
  },
  methods: {
    async loadAllData() {
      try {
        const response = await fetch("http://localhost:5000/all_data1");
        if (!response.ok) throw new Error("Network response was not ok");
        this.results = await response.json();
      } catch (error) {
        console.error("Error fetching all data:", error);
      }
    },
    async search() {
      if (this.query.trim().length < 1) {
        this.loadAllData();
        return;
      }
      try {
        const response = await fetch(`http://localhost:5000/search1?query=${encodeURIComponent(this.query)}`);
        if (!response.ok) throw new Error("Network response was not ok");
        this.results = await response.json();
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    },
    async viewCampaign(campaignId) {
      try {
        const response = await fetch(`http://localhost:5000/view_campaign1/${campaignId}`);
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        this.modalTitle = "Campaign Details";
        this.modalContent = `
          <p><strong>Name:</strong> ${data.name}</p>
          <p><strong>Description:</strong> ${data.description}</p>
          <p><strong>Start Date:</strong> ${data.start_date}</p>
          <p><strong>End Date:</strong> ${data.end_date}</p>
          <p><strong>Budget:</strong> ${data.budget}</p>
          <p><strong>Visibility:</strong> ${data.visibility}</p>
          <p><strong>Goals:</strong> ${data.goals}</p>
        `;
        this.showDetailsModal = true;
      } catch (error) {
        console.error("Error fetching campaign details:", error);
      }
    },
    async viewInfluencer(influencerId) {
      try {
        const response = await fetch(`http://localhost:5000/view_influencer1/${influencerId}`);
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        this.modalTitle = "Influencer Details";
        this.modalContent = `
          <p><strong>Username:</strong> ${data.username}</p>
          <p><strong>Name:</strong> ${data.name}</p>
          <p><strong>Niche:</strong> ${data.niche}</p>
          <p><strong>Category:</strong> ${data.category}</p>
          <p><strong>Reach:</strong> ${data.reach}</p>
          <p><strong>Platform Presence:</strong> ${data.platform_presence}</p>
        `;
        this.showDetailsModal = true;
      } catch (error) {
        console.error("Error fetching influencer details:", error);
      }
    },
    sendRequestForm(influencerId) {
      this.requestForm.influencerId = influencerId;
      this.requestForm.sponsorUsername = localStorage.getItem("username"); // Fetch sponsor username from localStorage
      this.showRequestModal = true;
    },
    async submitRequest() {
      try {
        const response = await fetch(`http://localhost:5000/send_request1/${this.requestForm.influencerId}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.requestForm),
        });
        const data = await response.json();
        if (data.success) {
          alert("Request sent successfully");
          this.closeModal();
        } else {
          alert("Error sending request");
        }
      } catch (error) {
        console.error("Error sending request:", error);
      }
    },
    closeModal() {
      this.showDetailsModal = false;
      this.showRequestModal = false;
    },
  },
  mounted() {
    // Fetch username from localStorage and set it
    this.name = localStorage.getItem("username");
    this.loadAllData();
  },
};
</script>


<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  max-width: 90%;
}
</style>
