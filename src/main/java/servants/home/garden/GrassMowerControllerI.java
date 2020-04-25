package servants.home.garden;

import Home.Garden.Coordinates;
import Home.Garden.GrassMower;
import Home.Garden.GrassMowerController;
import Home.InvalidCoordinates;
import com.zeroc.Ice.Current;

public class GrassMowerControllerI implements GrassMowerController {
    private final GrassMower grassMower;

    public GrassMowerControllerI() {
        grassMower = new GrassMower(new Coordinates(0, 0), false);
    }

    @Override
    public void turnSwitch(boolean isOn, com.zeroc.Ice.Current current) {
        grassMower.isOn = isOn;
    }

    @Override
    public Coordinates getCoordinates(com.zeroc.Ice.Current current) {
        return grassMower.coordinates;
    }

    @Override
    public void setCoordinates(Coordinates coordinates, Current current) throws InvalidCoordinates {
        if (!grassMower.isOn)
            throw new InvalidCoordinates("The grass mower engine is off. Unable to move.");
        else
            grassMower.coordinates = coordinates;
    }
}
