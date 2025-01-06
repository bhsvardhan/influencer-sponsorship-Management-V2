<template>
  <div class="container mt-5" style="max-height: 80vh; overflow-y: auto">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Influencer Dashboard</h1>
      <div class="btn-group">
        <router-link to="/influencer_dashboard" class="btn btn-hover">
          Profile
        </router-link>
        <br>
        <router-link to="/influencer_dashboard1" class="btn btn-info">
          Explore Campaigns
        </router-link>
        <br>
        <router-link to="/login" class="btn btn-hover">
          Logout
        </router-link>
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
        placeholder="Search campaigns or sponsors"
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
              View Campaign
            </button>
            <button
              v-if="item.type === 'sponsor'"
              @click="viewSponsor(item.id)"
              class="btn btn-info btn-sm"
            >
              View Sponsor
            </button>
            <button
              v-if="item.type === 'sponsor'"
              @click="sendRequestForm(item.id)"
              class="btn btn-primary btn-sm"
            >
              Send Request
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
            <label for="campaignName">Campaign Name:</label>
            <input
              v-model="requestForm.campaign_name"
              type="text"
              class="form-control"
              required
            />
          </div>
          <div class="form-group">
            <label for="message">Message:</label>
            <textarea
              v-model="requestForm.message"
              class="form-control"
              required
            ></textarea>
          </div>
          <div class="form-group">
            <label for="requirements">Your Skills:</label>
            <textarea
              v-model="requestForm.requirements"
              class="form-control"
              required
            ></textarea>
          </div>
          <div class="form-group">
            <label for="paymentAmount">Payment Amount:</label>
            <input
              v-model="requestForm.payment_amount"
              type="number"
              class="form-control"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" @click="closeModal" class="btn btn-secondary">
            Close
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "Influencer", // Placeholder name, replace with dynamic data
      query: "",
      results: [],
      showDetailsModal: false,
      showRequestModal: false,
      sponsorId: null, // ID of the selected sponsor for sending requests
      modalTitle: "",
      modalContent: "",
      requestForm: {
        campaign_name: "",
        message: "",
        requirements: "",
        payment_amount: "",
      },
    };
  },
  methods: {
    async loadAllData() {
      try {
        const response = await fetch("http://localhost:5000/all_data2");
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
        const response = await fetch(
          `http://localhost:5000/search2?query=${encodeURIComponent(
            this.query
          )}`
        );
        if (!response.ok) throw new Error("Network response was not ok");
        this.results = await response.json();
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    },
    async viewSponsor(sponsorId) {
      try {
        const response = await fetch(
          `http://localhost:5000/view_sponsor1/${sponsorId}`
        );
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        this.modalTitle = "Sponsor Details";
        this.modalContent = `
          <p><strong>Name:</strong> ${data.name}</p>
          <p><strong>Industry:</strong> ${data.industry}</p>
          <p><strong>Budget:</strong> ${data.budget}</p>
        `;
        this.showDetailsModal = true;
      } catch (error) {
        console.error("Error fetching sponsor details:", error);
        alert("Error loading sponsor details");
      }
    },
    sendRequestForm(sponsorId) {
      this.requestForm.sponsorId = sponsorId;
      this.requestForm.influencerUsername = localStorage.getItem("username")
      this.showRequestModal = true;
    },
    async submitRequest() {
      try {
        const response = await fetch(
          `http://localhost:5000/send_request2/${this.requestForm.sponsorId}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.requestForm),
          }
        );
        const data = await response.json();
        if (data.success) {
          alert("Request sent successfully");
          this.closeModal();
        } else {
          alert(data.message || "Error sending request");
        }
      } catch (error) {
        console.error("Error sending request:", error);
        alert("An error occurred while sending the request");
      }
    },
    closeModal() {
      this.showDetailsModal = false;
      this.showRequestModal = false;
      this.sponsorId = null;
      this.requestForm = {
        campaign_name: "",
        message: "",
        requirements: "",
        payment_amount: "",
      };
    },
  },
  mounted() {
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
