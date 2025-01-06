<template>
  <div class="admin-dashboard">
    <!-- Navigation Bar -->
    <nav class="nav-bar">
      <span
        class="nav-item"
        :class="{ active: currentTab === 'Info' }"
        @click="navigate('Info')"
        >Info</span
      >
      <span
        class="nav-item"
        :class="{ active: currentTab === 'Find' }"
        @click="navigate('Find')"
        >Find</span
      >
      <span
        class="nav-item"
        :class="{ active: currentTab === 'Stats' }"
        @click="navigate('Stats')"
        >Stats</span
      >
      <span class="nav-item" @click="$router.push('/login')">Logout</span>
    </nav>

    <!-- Page Content -->
    <div class="content">
      <h1>Admin's Dashboard</h1>

      <!-- Search Bar -->
      <div class="search-container">
        <input
          type="text"
          v-model="searchQuery"
          class="search-bar"
          placeholder="Search campaigns, influencers, or sponsors"
          @input="search"
        />
      </div>

      <!-- Results -->
      <div class="results-container">
        <div
          v-for="item in results"
          :key="item.id"
          :id="'item-' + item.id"
          class="result-item"
        >
          <span class="result-text">{{ item.type }} | {{ item.name }}</span>
          <button @click="viewItem(item.id)" class="view-btn">View</button>
          <button @click="flagItem(item.id)" class="flag-btn">Flag</button>
        </div>
        <div v-if="results.length === 0" class="no-results">
          No results found.
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
      currentTab: "Find",
      searchQuery: "",
      results: [],
    };
  },
  methods: {
    navigate(tab) {
      this.currentTab = tab;
      const routes = {
        Info: "/admin_dashboard",
        Find: "/admin_dashboard1",
        Stats: "/stats",
      };
      this.$router.push(routes[tab]);
    },
    logout() {
      axios
        .post("/logout")
        .then(() => this.$router.push("/login"))
        .catch((error) => console.error("Error during logout:", error));
    },
    search() {
      // Fetch data dynamically as the user types
      axios
        .get(
          `http://localhost:5000/admin_dashboard1?search_query=${encodeURIComponent(
            this.searchQuery
          )}`
        )
        .then((response) => {
          this.results = response.data.results || [];
        })
        .catch((error) => {
          console.error("Error fetching search results:", error);
          this.results = []; // Reset results on error
        });
    },
    viewItem(itemId) {
      axios
        .get(`http://localhost:5000/view/${itemId}`)
        .then((response) => {
          if (response.data.status === "success") {
            const itemType = response.data.type;
            const itemData = response.data.item_data;

            // Map database attribute names for each type
            const attributeMap = {
              campaign: [
                "Name",
                "Description",
                "Start Date",
                "End Date",
                "Budget",
                "Visibility",
                "Goals",
              ],
              influencer: [
                "Username",
                "Password",
                "Name",
                "Niche",
                "Category",
                "Reach",
                "Platform Presence",
                "Phone Number",
              ],
              sponsor: ["Username", "Password", "Name", "Industry", "Budget"],
            };

            // Mask the password field
            const attributes = attributeMap[itemType];
            const message = `
          Type: ${itemType.toUpperCase()}
          Attributes:
          ${attributes
            .map(
              (attr, index) =>
                `${attr}: ${attr === "Password" ? "****" : itemData[index]}`
            )
            .join("\n")}
        `;

            alert(message);
          } else {
            alert(`Error: ${response.data.message}`);
          }
        })
        .catch((error) => {
          alert(
            `An error occurred: ${
              error.response ? error.response.data.message : error.message
            }`
          );
        });
    },

    flagItem(itemId) {
      const confirmed = confirm("Are you sure you want to flag this item?");
      if (confirmed) {
        axios
          .post(`http://localhost:5000/flag/${itemId}`)
          .then(() => {
            alert("Item flagged successfully!");
            this.results = this.results.filter((item) => item.id !== itemId);
          })
          .catch((error) => {
            console.error("Error flagging item:", error);
            alert("Failed to flag the item.");
          });
      }
    },
  },
  mounted() {
    this.search(); // Load all data on mount (empty query initially fetches everything)
  },
};
</script>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: space-between;
}
.nav-item {
  cursor: pointer;
  padding: 10px;
}
.nav-item.active {
  background-color: #007bff;
  color: white;
}
.content {
  margin: 20px;
}
.search-container {
  margin-bottom: 20px;
}
.search-bar {
  width: 100%;
  padding: 10px;
  font-size: 16px;
}
.results-container {
  display: flex;
  flex-direction: column;
}
.result-item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
}
.view-btn,
.flag-btn {
  margin-left: 10px;
}
.no-results {
  text-align: center;
  font-size: 18px;
}
</style>
