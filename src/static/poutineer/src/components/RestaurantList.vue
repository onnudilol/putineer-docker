<template>
  <b-container>
    <div id="map"></div>
    <hr>
    <h1>Poutine near {{ currentCity }}</h1>
    <div
      class="card"
      v-for="restaurant of restaurants"
      v-bind:key="restaurant.id"
      v-bind:id="restaurant.yelp_id"
    >
      <div class="card-header">
        <a :href=restaurant.image_url>
          <b-img-lazy class="restaurant-thumbnail" thumbnail fluid width="128" height="128" :src=restaurant.image_url>
        </a>
        <h3>{{ restaurant.name }} <span v-if="restaurant.verified" title="Verified">✅</span></h3>
      </div>
      <div class="card-body">
        <p>{{ restaurant.address }}</p>
        <p>{{ restaurant.distance }} km away</p>
      </div>
    </div>
  </b-container>
</template>

<script>
import axios from "axios";
import "leaflet";

export default {
  name: "RestaurantList",

  data() {
    return {
      currentCity: "",
      coords: [],
      restaurants: [],
      map: null,
      tileLayer: null,
      layers: [
        {
          id: 0,
          name: "Restaurants",
          active: true,
          features: []
        }
      ]
    };
  },

  created: function() {
    // bind self to this because this won't work in callbacks
    let self = this;

    // get user position
    navigator.geolocation.getCurrentPosition(function(position) {
      self.coords = [
        parseFloat(position.coords.latitude),
        parseFloat(position.coords.longitude)
      ];

      let params = { lat: self.coords[0], lon: self.coords[1] };

      axios.get("http://localhost/api", { params }).then(function(response) {
        self.restaurants = response.data.slice(0, -1);

        // duplicate restaurants and add the fields that leaflet wants
        self.layers[0].features = self.restaurants;
        self.layers[0].features.forEach(element => {
          element.type = "marker";
        });

        self.currentCity =
          response.data[response.data.length - 1].current_address;

        // initialize map
        self.map = L.map("map").setView(self.coords, 12);
        self.tileLayer = L.tileLayer(
          "https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png",
          {
            maxZoom: 18,
            attribution:
              '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>'
          }
        );

        // initialize layers
        self.tileLayer.addTo(self.map);

        // coloured icons from https://github.com/pointhi/leaflet-color-markers
        let redIcon = new L.Icon({
          iconUrl:
            "https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
          shadowUrl:
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });

        // marker for current coords
        let currentPosMarker = L.marker(self.coords, {icon: redIcon}).bindPopup('Current Position')
        currentPosMarker.addTo(self.map);

        // markers for restaurants
        self.layers.forEach(layer => {
          const markerFeatures = layer.features.filter(
            feature => feature.type === "marker"
          );

          markerFeatures.forEach(feature => {
            feature.leafletObject = L.marker(feature.coords).bindPopup(
              '<a href="' + '#' + feature.yelp_id + '">' + feature.name + '</a>'
            );
            feature.leafletObject.addTo(self.map);
          });
        });
      });
    });
  }
};
</script>

<style lang="scss" scoped>
.card { 
  border-color: #d50000;
  margin: 1rem;
}

.card-header {
  background-color: #f44336;
}

.card-body {
  padding: 1rem;
}

.restaurant-thumbnail {
  margin-bottom: 0.5rem;
}
</style>
