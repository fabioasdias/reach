import React from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import './glmap.css';


mapboxgl.accessToken = 'pk.eyJ1IjoiZGlhc2YiLCJhIjoiY2pqc243cW9wNDN6NTNxcm1jYW1jajY2NyJ9.2C0deXZ03NJyH2f51ui4Jg';



let Map = class Map extends React.Component {
  constructor(props){
    super(props);
    this.state={map:undefined}
  }

    
  componentDidUpdate() {
  }

  componentWillUpdate(nextProps, nextState) {
    if ((this.moving!==undefined)&&(this.moving)){
      return;
    }
    if (nextProps.boundsCallback!==undefined){
      nextProps.boundsCallback(undefined);
    }
  }


  componentDidMount() {
    this.map = new mapboxgl.Map({
      container: this.mapContainer,
      style: 'mapbox://styles/mapbox/light-v9',
      center: [-99.0524136, 38.998221],
      maxZoom: 10,
      minZoom: 4,
      zoom:4,
    });

    // // just to show how it can be done
    // navigator.geolocation.getCurrentPosition((d)=>{
    //   this.moving=true;
    //   // this.map.setZoom(12);
    //   this.map.flyTo({
    //     center: [
    //         d.coords.longitude,
    //         d.coords.latitude,
    //         ]});
    //     });
    // this.moving=false;

    //Use this callback to syncronize views across different maps
    let BoundsChange=(d)=>{
      if (d.originalEvent!==undefined){//&&(this.moving===false))  
        if (this.props.boundsCallback!==undefined){
          this.props.boundsCallback(this.map.getBounds());
        }
      }
    }

    this.map.on('dragend', BoundsChange);
    this.map.on('zoomend', BoundsChange);    
    this.map.on('movestart',()=>{this.moving=true;});
    this.map.on('moveend',()=>{this.moving=false;});
    this.map.on('click',(e)=>{
      // this.map.flyTo({center:[e.lngLat.lng,e.lngLat.lat]});
      var features = this.map.queryRenderedFeatures(e.point, { layers: ['zcta'] });
      console.log(features);
      if (features.length>0){
        if (this.props.clbClick!==undefined){
          //pass the properties of the geometry clicked back to the "above"
          //object. Lazy way of not using react-redux. But also leaves this object more flexible
          this.props.clbClick(features[0].properties);
        }
      }
    });
    // properties.ZCTA5CE10

    this.map.on('load', () => {
      this.map.addSource('gj', {
        type: 'vector',
        url: 'mapbox://diasf.4ns42s1r'
      });
    
      this.map.addLayer({
        id: 'zcta',
        type: 'fill',
        source: 'gj', 
        "source-layer": "ZCTA2016-cip2yb",
        //https://www.mapbox.com/mapbox-gl-js/style-spec/#layers-fill
        paint: {
          'fill-color':'lightgray',
          'fill-outline-color':'black',
          'fill-opacity' : 0.5,
        }            
      }, 'country-label-lg'); 
      this.setState({'map':this.map});
    });
  }

  render() {
    return (
      <div ref={el => this.mapContainer = el} 
      className={(this.props.className!==undefined)?this.props.className:"absolute top right left bottom"}
      />
    );
  }
}


export default Map;
