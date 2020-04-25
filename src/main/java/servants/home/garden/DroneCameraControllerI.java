package servants.home.garden;

import Home.Direction;
import Home.Garden.Coordinates;
import Home.Garden.DroneCamera;
import Home.Garden.DroneCameraController;
import Home.InvalidCoordinates;
import com.zeroc.Ice.Current;

public class DroneCameraControllerI implements DroneCameraController {
    private final DroneCamera drone;

    public DroneCameraControllerI() {
        drone = new DroneCamera(new Coordinates(0, 0), Direction.North, 0, 0);
    }

    @Override
    public double getAltitude(com.zeroc.Ice.Current current) {
        return drone.altitude;
    }

    @Override
    public void setAltitude(double altitude, Current current) throws InvalidCoordinates {
        if (altitude < 0)
            throw new InvalidCoordinates("Altitude must not be negative.");

        this.drone.altitude = altitude;
    }

    @Override
    public Direction getDirection(com.zeroc.Ice.Current current) {
        return drone.direction;
    }

    @Override
    public long getZoom(com.zeroc.Ice.Current current) {
        return drone.zoom;
    }

    @Override
    public void setDirection(Direction direction, com.zeroc.Ice.Current current) {
        drone.direction = direction;
    }

    @Override
    public void zoomIn(long zoomBy, com.zeroc.Ice.Current current) {
        drone.zoom += zoomBy;
    }

    @Override
    public void zoomOut(long zoomBy, com.zeroc.Ice.Current current) {
        drone.zoom -= zoomBy;
    }

    @Override
    public Coordinates getCoordinates(com.zeroc.Ice.Current current) {
        return drone.coordinates;
    }

    @Override
    public void setCoordinates(Coordinates coordinates, Current current) throws InvalidCoordinates {
        if (coordinates.latitude < 0 || coordinates.longitude < 0) // just random predicate, for test
            throw new InvalidCoordinates("Drone accepts only positive coordinates");

        drone.coordinates = coordinates;
    }
}
