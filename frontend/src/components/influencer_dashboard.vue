<template>
  <div class="container mt-5" style="max-height: 80vh; overflow-y: auto">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Influencer Dashboard</h1>
      <div class="btn-group">
        <router-link to="/profile" class="btn btn-info">Profile</router-link>
        <br />
        <router-link to="/find" class="btn btn-hover">Find</router-link>
        <br />
        <router-link to="/login" class="btn btn-hover">Logout</router-link>
      </div>
    </div>

    <div class="mx-auto">
      <span class="display-2">Welcome {{ userName }}</span>
    </div>

    <h2>Active Campaigns</h2>
    <div class="row">
      <div
        v-for="campaign in campaigns"
        :key="campaign.id"
        class="col-md-12 mb-3"
      >
        <div class="card">
          <div
            class="card-body d-flex justify-content-between align-items-center"
          >
            <div>
              <h5 class="card-title">{{ campaign.name }}</h5>
              <div class="progress">
                <div
                  class="progress-bar"
                  :style="{
                    width:
                      calculateProgress(
                        campaign.start_date,
                        campaign.end_date
                      ) + '%',
                  }"
                  role="progressbar"
                  :aria-valuenow="
                    calculateProgress(campaign.start_date, campaign.end_date)
                  "
                  aria-valuemin="0"
                  aria-valuemax="100"
                >
                  {{
                    calculateProgress(
                      campaign.start_date,
                      campaign.end_date
                    ).toFixed(2)
                  }}%
                </div>
              </div>
            </div>
            <button
              @click="viewCampaign(campaign.name)"
              class="btn btn-primary"
            >
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>

    <h2>My Events</h2>
    <div id="eventsContainer" class="row">
      <div v-for="event in events" :key="event.id" class="col-md-12 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ event.campaign_name }}</h5>
            <p><strong>Sponsor:</strong> {{ event.sponsor_username }}</p>
          </div>
        </div>
      </div>
    </div>

    <h2>New Requests</h2>
    <div id="requestsContainer" class="row">
      <div
        v-for="request in requests"
        :key="`${request.campaign_name}-${request.influencer_username}`"
        class="col-md-12 mb-3"
      >
        <div class="card">
          <div
            class="card-body d-flex justify-content-between align-items-center"
          >
            <div>
              <h5 class="card-title">
                {{ request.campaign_name }} - {{ request.influencer_username }}
              </h5>
              <p><strong>Messages:</strong> {{ request.messages }}</p>
              <p><strong>Requirements:</strong> {{ request.requirements }}</p>
              <p>
                <strong>Payment Amount:</strong> ${{ request.payment_amount }}
              </p>
              <p><strong>Status:</strong> {{ request.status }}</p>
            </div>
            <div>
              <button
                @click="viewCampaign(request.campaign_name)"
                class="btn btn-info"
              >
                View Campaign
              </button>
              <button
                @click="
                  acceptRequest(
                    request.campaign_name,
                    request.influencer_username
                  )
                "
                class="btn btn-success"
              >
                Accept
              </button>
              <button
                @click="
                  rejectRequest(
                    request.campaign_name,
                    request.influencer_username
                  )
                "
                class="btn btn-danger"
              >
                Reject
              </button>
            </div>
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
      userName: "",
      campaigns: [],
      events: [],
      requests: [],
      campaignInfo: {},
    };
  },
  methods: {
    fetchDashboardData() {
      axios
        .get("http://localhost:5000/influencer_dashboard")
        .then((response) => {
          this.campaigns = response.data.campaigns;
          this.userName = localStorage.getItem("username");
        });
    },
    fetchRequests() {
      const influencerUsername = localStorage.getItem("username");
      axios
        .get(
          `http://localhost:5000/view_requests_influencer?influencer_username=${influencerUsername}`
        )
        .then((response) => {
          if (response.data.requests) {
            this.requests = response.data.requests;
          }
        })
        .catch(() => {
          alert("Failed to fetch requests.");
        });
    },
    fetchEvents() {
      axios.get("http://localhost:5000/fetch_events").then((response) => {
        if (response.data.events) {
          this.events = response.data.events;
        }
      });
    },
    calculateProgress(startDate, endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      const today = new Date();

      const totalDuration = (end - start) / (1000 * 60 * 60 * 24);
      const elapsedDuration = (today - start) / (1000 * 60 * 60 * 24);

      return Math.max(
        0,
        Math.min((elapsedDuration / totalDuration) * 100, 100)
      );
    },
    viewCampaign(campaignName) {
      axios
        .post("http://localhost:5000/current_campaigns", {
          campaign_name: campaignName,
        })
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
        .post("http://localhost:5000/accept_request_influencer", {
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
        .post("http://localhost:5000/reject_request_influencer", {
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
    this.fetchEvents();
  },
};
</script>

<style></style>
