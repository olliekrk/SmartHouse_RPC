#ifndef SMART_DEVICES
#define SMART_DEVICES

module Home {
    enum TemperatureUnit { Fahrenheit, Celsius }
	enum Direction { North, West, East, South }

    exception HomeException {
        string reason;
    }

    exception InvalidQuantity extends HomeException {}
    exception InvalidCoordinates extends HomeException {}
    exception InvalidTemperature extends HomeException {
        double maxValue;
        double minValue;
    }

    module Garden {
        struct Coordinates {
                double latitude;
                double longitude;
        }

        class GrassMower {
	        Coordinates coordinates;
            bool isOn;
        }

        interface Localizable {
            Coordinates getCoordinates();
            void setCoordinates(Coordinates coordinates) throws InvalidCoordinates;
        }

        interface GrassMowerController extends Localizable {
            void turnSwitch(bool isOn);
        }

        class Camera {
    	    Coordinates coordinates;
            Direction direction;
            long zoom;
        }

        class WallCamera extends Camera {
            bool visible;
        }

        class DroneCamera extends Camera {
            double altitude;
        }

        interface CameraController extends Localizable {
            Direction getDirection();
            long getZoom();

            void setDirection(Direction direction);
            void zoomIn(long zoomBy);
            void zoomOut(long zoomBy);
        }

        interface WallCameraController extends CameraController {
            bool isVisible();
            void setVisibility(bool visible);
        }

        interface DroneCameraController extends CameraController {
            double getAltitude();
            void setAltitude(double altitude) throws InvalidCoordinates;
        }
    }

    module Kitchen {
        struct Item {
            string name;
        }

        struct Temperature {
            TemperatureUnit unit;
            double value;
        }

        dictionary<Item, long> ItemBag;

        class Fridge {
	        ItemBag items;
            Temperature temperature;
            string messageOfTheDay;
            bool ecoMode;
        }

	    interface FridgeController {
	        Temperature getTemperature(TemperatureUnit unit);
            string getMessageOfTheDay();
            ItemBag getItems();

            void setEcoMode(bool ecoMode);
            void setTemperature(Temperature temperature) throws InvalidTemperature;

            void putItems(Item item, long quantity) throws InvalidQuantity;
            void removeItems(Item item, long quantity) throws InvalidQuantity;
	    }
    }

    sequence<string> ObjectIdentities;
    interface HomeStatus {
        ObjectIdentities getActiveDevices();
    }
}


#endif // SMART_DEVICES
