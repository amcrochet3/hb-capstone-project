function initMap() {
    const farnsworthHouseCoordinates = {
        lat: 41.6357653112787,
        lng: -88.53572671534454
    };

    const basicMap = new google.maps.Map(document.querySelector('#map'), {
        center: farnsworthHouseCoordinates,
        zoom: 10
    });

    const farnsworthMarker = new google.maps.Marker({
        position: farnsworthHouseCoordinates,
        title: 'Farnsworth House',
        map: basicMap
    });

    farnsworthMarker.addListener('click', () => {
        alert('This house is iconic.');
    });

    const farnsworthInfo = new google.maps.InfoWindow({
        content: '<h1>Edith Farnsworth House</h1>'
    });

    farnsworthInfo.open(basicMap, farnsworthMarker);
}