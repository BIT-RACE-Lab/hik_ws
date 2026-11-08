package Commom;

import javax.xml.xpath.*;
import javax.xml.namespace.NamespaceContext;
import java.util.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;

public class xmlParse {

    public static class TrafficDataResult {
        public String searchID;
        public Map<String, String> fields;

        public TrafficDataResult(String searchID, Map<String, String> fields) {
            this.searchID = searchID;
            this.fields = fields;
        }
    }

    public static TrafficDataResult extractFields(String xml, int n, List<String> fieldNames) {
        try {
            // 1. 解析XML
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setNamespaceAware(true);
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(new ByteArrayInputStream(xml.getBytes("UTF-8")));
            XPathFactory xpathFactory = XPathFactory.newInstance();
            XPath xpath = xpathFactory.newXPath();
            xpath.setNamespaceContext(new NamespaceContext() {
                public String getNamespaceURI(String prefix) {
                    if ("ns".equals(prefix)) return "http://www.isapi.org/ver20/XMLSchema";
                    return javax.xml.XMLConstants.NULL_NS_URI;
                }

                public String getPrefix(String uri) { return null; }
                public Iterator<String> getPrefixes(String uri) { return null; }
            });

            // 2. 提取 searchID
            XPathExpression searchIdExpr = xpath.compile("/ns:TrafficSearchResult/ns:searchID");
            String searchID = (String) searchIdExpr.evaluate(doc, XPathConstants.STRING);

            // 3. 提取多个字段
            Map<String, String> fieldMap = new LinkedHashMap<>();
            for (String field : fieldNames) {
                String expression = String.format(
                        "/ns:TrafficSearchResult/ns:matchList/ns:matchElement[%d]/ns:trafficData/ns:%s",
                        n + 1, field);
                XPathExpression fieldExpr = xpath.compile(expression);
                String value = (String) fieldExpr.evaluate(doc, XPathConstants.STRING);
                fieldMap.put(field, value);
            }

            return new TrafficDataResult(searchID, fieldMap);

        } catch (Exception e) {
            e.printStackTrace();
            return new TrafficDataResult(null, Collections.emptyMap());
        }
    }
}