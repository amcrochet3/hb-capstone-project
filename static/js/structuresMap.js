function initMap() {
    const coords = { lat: 41.6357653112787, lng: -88.5356838 };
    const basicMap = new google.maps.Map(document.querySelector("#map"), {
        center: coords,
        zoom: 3,
    });

    let markers = [];
    let currentInfoWindow = null;

    fetch("/map_data")
        .then((response) => response.json())
        .then((data) => {
            const locations = data;

            for (const location of locations) {
                const marker = new google.maps.Marker({
                    title: location.structure_name,
                    position: { lat: location.lat, lng: location.lng },
                    map: basicMap,
                    icon: {
                        url: "/static/img/marker.svg",
                        scaledSize: {
                            width: 30,
                            height: 30,
                        },
                    },
                });

                const infoWindow = new google.maps.InfoWindow({
                    maxWidth: 200,
                });

                marker.addListener("click", () => {
                    if (currentInfoWindow) {
                        currentInfoWindow.close();
                    }

                    if (currentInfoWindow !== infoWindow) {
                        const geocoder = new google.maps.Geocoder();
                        geocoder.geocode({ location: marker.position }, (results) => {
                            const address = results && results[0] && results[0].formatted_address;
                            if (address) {
                                const markerInfo = `
                    <div id="content">
                      <h1>${marker.title}</h1>
                      <p>${address}</p>
                    </div>
                  `;

                                infoWindow.setContent(markerInfo);
                                infoWindow.open(basicMap, marker);
                                currentInfoWindow = infoWindow;
                            }
                        });
                    } else {
                        currentInfoWindow = null;
                    }
                });

                markers.push(marker);
            }
        });
}


