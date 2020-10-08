import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
import styled from "styled-components";

import { colors } from "../../Constants";
import { MainCanvas, ImageGrid } from "./Components";
import { ImageLabeler, ImageData, Annotation } from "../../assets/js/klabel.js";
import { Button, Select } from "../../Components";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  background-color: white;
`;

const SubContainer = styled.div`
  display: flex;
  flex-direction: row;
  background-color: white;
  margin-left: 3vw;
  margin-top: 3vh;
`;

const ImageGridContainer = styled.div`
  width: 100%;
  height: 75vh;
  margin-top: 2vh;
  margin-right: 3vw;
  margin-left: 3vw;
  border-radius: 5px;
`;

const TitleHeader = styled.h1`
  font-family: "AirBnbCereal-Medium";
  font-size: 24px;
  color: ${colors.primary};
  padding-right: 20px;
`;

const OptionsSelect = styled(Select)`
  font-size: 13px;
  height: 28px;
  padding: 0 5px;
`;

const Slider = styled.input`
  width: 20%; /* Full-width */
  height: 25px; /* Specified height */
  border-radius: 5px;
  margin-left: 20px;
`;

function LabelingPage() {
  const location = useLocation();
  const datasetName = location.state.datasetName;
  const paths = location.state.paths;
  const identifiers = location.state.identifiers;

  /* Klabel stuff */
  const labeler = new ImageLabeler();
  const main_canvas_id = 'main_canvas';

  // Annotating vs Exploring
  var forager_mode = 'forager_annotate';
  var image_size = 150;

  const image_data = [];
  for (let i=0; i<paths.length; i++) {
    const data = new ImageData();
    data.source_url = paths[i];
    image_data.push(data);
  }

  const onImageClick = (idx) => {
    labeler.set_current_frame_num(idx);
  }

  useEffect(() => {
    const handle_clear_boxes = () => {
      labeler.clear_boxes();
    }

    const toggle_extreme_points_display = () => {
      const button = document.getElementById("toggle_pt_viz_button");
      const new_status = !button.toggle_status;
      labeler.set_extreme_points_viz(new_status);
      button.toggle_status = new_status;

      if (new_status === false) {
        button.innerHTML = 'Show Extreme Points';
      } else {
        button.innerHTML = 'Hide Extreme Points';
      }
    }

    const toggle_letterbox = () => {
      const button = document.getElementById("toggle_letterbox_button");
      const new_status = !button.toggle_status; 
      labeler.set_letterbox(new_status);
      button.toggle_status = new_status;

      if (new_status === false) {
        button.innerHTML = 'Use Letterbox View';
      } else {
        button.innerHTML = 'Use Scaled View';
      }
    }

    const handle_mode_change = () => {
      const select = document.getElementById("select_annotation_mode");
      if (select.value.localeCompare("box_extreme_points") === 0) {
        labeler.set_annotation_mode(Annotation.ANNOTATION_MODE_EXTREME_POINTS_BBOX);
      } else if (select.value.localeCompare("box_two_points") === 0) {
        labeler.set_annotation_mode(Annotation.ANNOTATION_MODE_TWO_POINTS_BBOX);
      } else if (select.value.localeCompare("point") === 0) {
        labeler.set_annotation_mode(Annotation.ANNOTATION_MODE_POINT);
      } else if (select.value.localeCompare("per_frame") === 0) {
        labeler.set_annotation_mode(Annotation.ANNOTATION_MODE_PER_FRAME_CATEGORY);
        labeler.set_categories( { true: { idx: 1, color: "#67bf5c" }, false: {idx:2, color: "#ed665d"} } );
      }
    }

    const handle_get_annotations = () => {
      const results = labeler.get_annotations();
      console.log(results);
    }
    
    const handle_image_size = () => {
      image_size = document.getElementById("image_size").value;
      var toChange = document.querySelectorAll(".grid_item");
      for (var i = 0; i < toChange.length; i++) {
        toChange[i].style.height = image_size + "px"
      }
    }

    const main_canvas = document.getElementById(main_canvas_id);
    labeler.init(main_canvas);

    const handle_forager_change = () => {
      const select = document.getElementById("select_forager_mode");
      const klabeldiv = document.getElementById("klabel_wrapper");
      if (select.value.localeCompare("forager_annotate") === 0) {
        forager_mode = "forager_annotate"
        klabeldiv.style.display = "flex"
      } else if (select.value.localeCompare("forager_explore") === 0) {
        forager_mode = "forager_explore"
        klabeldiv.style.display = "none"
      } 
    }

    labeler.load_image_stack(image_data);

    labeler.set_annotation_mode(Annotation.ANNOTATION_MODE_EXTREME_POINTS_BBOX);

    let button = document.getElementById("toggle_pt_viz_button");
    button.onclick = toggle_extreme_points_display;
    button.toggle_status = true;
    labeler.set_extreme_points_viz(button.toggle_status);

    button = document.getElementById("toggle_sound_button");
    button.toggle_status = false;
    labeler.set_play_audio(button.toggle_status);

    button = document.getElementById("toggle_letterbox_button");
    button.onclick = toggle_letterbox;
    button.toggle_status = true;
    labeler.set_letterbox(button.toggle_status);

    button = document.getElementById("clear_button");
    button.onclick = handle_clear_boxes;

    button = document.getElementById("get_annotations");
    button.onclick = handle_get_annotations;

    let select = document.getElementById("select_annotation_mode")
    select.onchange = handle_mode_change;

    select = document.getElementById("select_forager_mode")
    select.onchange = handle_forager_change;

    let image_size = document.getElementById("image_size")
    image_size.oninput = handle_image_size;

    window.addEventListener("keydown", function(e) {
      e.preventDefault();
      labeler.handle_keydown(e);
    });

    window.addEventListener("keyup", function(e) {
      e.preventDefault();
      labeler.handle_keyup(e);
    });
  }, [labeler, image_data]);

  return (
    <Container>
      <SubContainer>
        <TitleHeader>Labeling: {datasetName}</TitleHeader>
        <OptionsSelect alt="true" id="select_forager_mode">
          <option value="forager_annotate">Annotate</option>
          <option value="forager_explore">Explore</option>
        </OptionsSelect>

        <label style={{"fontSize": '25px',"marginLeft": "260px"}}>Image Size</label>
        <Slider type="range" min="50" max="300" defaultValue="100" id="image_size"></Slider>
      </SubContainer>
      <SubContainer>
        <MainCanvas/>
        <ImageGridContainer>
          <ImageGrid datasetName={datasetName} onImageClick={onImageClick} imageHeight={image_size}/>
        </ImageGridContainer>
      </SubContainer>
    </Container>
  );
};

export default LabelingPage;