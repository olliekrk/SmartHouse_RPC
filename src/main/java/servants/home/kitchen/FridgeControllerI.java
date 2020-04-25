package servants.home.kitchen;

import Home.InvalidQuantity;
import Home.InvalidTemperature;
import Home.Kitchen.Fridge;
import Home.Kitchen.FridgeController;
import Home.Kitchen.Item;
import Home.Kitchen.Temperature;
import Home.TemperatureUnit;
import com.zeroc.Ice.Current;

import java.util.HashMap;
import java.util.Map;

public class FridgeControllerI implements FridgeController {
    private final static long MAX_ITEM_QUANTITY = 10;
    private final Fridge fridge;

    public FridgeControllerI() {
        fridge = initialFridge();
    }

    @Override
    public Temperature getTemperature(TemperatureUnit unit, com.zeroc.Ice.Current current) {
        return fridge.temperature;
    }

    @Override
    public String getMessageOfTheDay(com.zeroc.Ice.Current current) {
        return messageOfTheDay(fridge.ecoMode);
    }

    @Override
    public Map<Item, Long> getItems(com.zeroc.Ice.Current current) {
        return fridge.items;
    }

    @Override
    public void setEcoMode(boolean ecoMode, com.zeroc.Ice.Current current) {
        fridge.ecoMode = ecoMode;
    }

    @Override
    public void setTemperature(Temperature temperature, com.zeroc.Ice.Current current) throws InvalidTemperature {
        switch (temperature.unit) {
            case Celsius:
                if (temperature.value > 15 || temperature.value < -10)
                    throw new InvalidTemperature("Temperature in Celsius out of range.", 15, -10);
                break;
            case Fahrenheit:
                if (temperature.value > 800 || temperature.value < 0)
                    throw new InvalidTemperature("Temperature in Fahrenheit out of range.", 800, 0);
        }

        this.fridge.temperature = temperature;
    }

    @Override
    public void putItems(Item item, long quantity, Current current) throws InvalidQuantity {
        var newQuantity = fridge.items.getOrDefault(item, 0L) + quantity;
        if (newQuantity <= 0 || newQuantity > MAX_ITEM_QUANTITY) {
            throw new InvalidQuantity("The item quantity to add must be positive and must not exceed " + MAX_ITEM_QUANTITY);
        }
        fridge.items.put(item, newQuantity);
    }

    @Override
    public void removeItems(Item item, long quantity, Current current) throws InvalidQuantity {
        var currentQuantity = fridge.items.getOrDefault(item, 0L);
        if (currentQuantity - quantity < 0) {
            throw new InvalidQuantity("There are too few items in the fridge: " + fridge.items.getOrDefault(item, 0L));
        }
        fridge.items.put(item, currentQuantity - quantity);
    }

    private static Fridge initialFridge() {
        return new Fridge(
                new HashMap<>(),
                new Temperature(TemperatureUnit.Celsius, 4),
                messageOfTheDay(true),
                true
        );
    }

    private static String messageOfTheDay(boolean ecoMode) {
        return String.format("Hello Fridge! The eco mode is: %s", ecoMode ? "ON" : "OFF");
    }
}
