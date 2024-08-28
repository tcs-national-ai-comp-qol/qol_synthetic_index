from pathlib import Path
import json
import jsonschema

QOL_JSON_SCHEMA = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "array",
  "items": [
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    },
    {
      "type": "object",
      "properties": {
        "answer": {
          "type": "object",
          "properties": {
            "QoL": {
              "type": "integer"
            },
            "a_sense_of_control": {
              "type": "object",
              "properties": {
                "cost_of_living": {
                  "type": "integer"
                },
                "essential_services": {
                  "type": "integer"
                },
                "influence_and_contribution": {
                  "type": "integer"
                },
                "safety": {
                  "type": "integer"
                }
              },
              "required": [
                "cost_of_living",
                "essential_services",
                "influence_and_contribution",
                "safety"
              ]
            },
            "a_sense_of_wonder": {
              "type": "object",
              "properties": {
                "distinctive_design_and_culture": {
                  "type": "integer"
                },
                "play_and_recreation": {
                  "type": "integer"
                }
              },
              "required": [
                "distinctive_design_and_culture",
                "play_and_recreation"
              ]
            },
            "connected_communities": {
              "type": "object",
              "properties": {
                "belonging": {
                  "type": "integer"
                },
                "local_business_and_jobs": {
                  "type": "integer"
                }
              },
              "required": [
                "belonging",
                "local_business_and_jobs"
              ]
            },
            "connection_to_nature": {
              "type": "object",
              "properties": {
                "biodiversity": {
                  "type": "integer"
                },
                "climate_resilience_and_adaptation": {
                  "type": "integer"
                },
                "green_and_blue_spaces": {
                  "type": "integer"
                }
              },
              "required": [
                "biodiversity",
                "climate_resilience_and_adaptation",
                "green_and_blue_spaces"
              ]
            },
            "getting_around": {
              "type": "object",
              "properties": {
                "car": {
                  "type": "integer"
                },
                "public_transport": {
                  "type": "integer"
                },
                "walking_and_cycling": {
                  "type": "integer"
                }
              },
              "required": [
                "car",
                "public_transport",
                "walking_and_cycling"
              ]
            },
            "health_equity": {
              "type": "object",
              "properties": {
                "air_noise_light": {
                  "type": "integer"
                },
                "food_choice": {
                  "type": "integer"
                },
                "housing_standard": {
                  "type": "integer"
                }
              },
              "required": [
                "air_noise_light",
                "food_choice",
                "housing_standard"
              ]
            }
          },
          "required": [
            "QoL",
            "a_sense_of_control",
            "a_sense_of_wonder",
            "connected_communities",
            "connection_to_nature",
            "getting_around",
            "health_equity"
          ]
        },
        "query": {
          "type": "string"
        }
      },
      "required": [
        "answer",
        "query"
      ]
    }
  ]
}




QOL_DATA_DIR = Path("qol_dataset").glob("*.json")
NUM_CITIES = 10


erroneous_files = []

for file in QOL_DATA_DIR:
    try:
        data = json.loads(file.read_text())
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file}: {e}")
        erroneous_files.append(file)
        continue

    # if the data is not adherant to the JSON schema, then we will add it to the erroneous files
    try:
        jsonschema.validate(data, QOL_JSON_SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        print(f"Data does not adhere to the JSON schema in {file}: {e}")
        erroneous_files.append(file)
        continue

Path("erroneous_files.txt").write_text("\n".join(map(str, erroneous_files)))