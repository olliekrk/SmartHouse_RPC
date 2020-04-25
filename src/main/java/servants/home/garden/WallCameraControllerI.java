package servants.home.garden;

import Home.Direction;
import Home.Garden.Coordinates;
import Home.Garden.WallCamera;
import Home.Garden.WallCameraController;
import Home.InvalidCoordinates;
import com.zeroc.Ice.Current;

public class WallCameraControllerI implements WallCameraController {
    private final WallCamera camera;

    public WallCameraControllerI() {
        camera = new WallCamera(new Coordinates(0, 0), Direction.North, 0, true);
    }

    @Override
    public boolean isVisible(com.zeroc.Ice.Current current) {
        return camera.visible;
    }

    @Override
    public void setVisibility(boolean visible, com.zeroc.Ice.Current current) {
        camera.visible = visible;
    }

    @Override
    public Direction getDirection(com.zeroc.Ice.Current current) {
        return camera.direction;
    }

    @Override
    public long getZoom(com.zeroc.Ice.Current current) {
        return camera.zoom;
    }

    @Override
    public void setDirection(Direction direction, com.zeroc.Ice.Current current) {
        camera.direction = direction;
    }

    @Override
    public void zoomIn(long zoomBy, com.zeroc.Ice.Current current) {
        camera.zoom += zoomBy;
    }

    @Override
    public void zoomOut(long zoomBy, com.zeroc.Ice.Current current) {
        camera.zoom -= zoomBy;
    }

    @Override
    public Coordinates getCoordinates(com.zeroc.Ice.Current current) {
        return camera.coordinates;
    }

    @Override
    public void setCoordinates(Coordinates coordinates, Current current) throws InvalidCoordinates {
        throw new InvalidCoordinates("Wall camera is fixed to the wall. How is it supposed to move?");
    }
}
